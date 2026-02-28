# study_engine/gui_player.py
# ───────────────────────────
# GUIExplanationPlayer — drives chunked, non-blocking TTS playback.
# Called from the UI; bridges AIExplainer + AudioController + StateManager.

from __future__ import annotations
from PySide6.QtCore import QObject, QThread, Signal

from study_engine.audio.audio_controller import AudioController
from study_engine.state_manager import StateManager


# ── Background LLM Worker ────────────────────────────────────────────────────

class LLMWorker(QThread):
    """Calls AIExplainer.explain() in a background thread."""

    result_ready = Signal(str)
    error        = Signal(str)

    def __init__(self, explainer, paragraph_text: str, parent=None):
        super().__init__(parent)
        self._explainer = explainer
        self._text = paragraph_text

    def run(self):
        try:
            explanation = self._explainer.explain(self._text)
            self.result_ready.emit(explanation)
        except Exception as exc:
            self.error.emit(str(exc))


class LLMDoubtWorker(QThread):
    """Calls AIExplainer.explain_doubt() in a background thread."""

    result_ready = Signal(str)
    error        = Signal(str)

    def __init__(self, explainer, doubt_text: str, parent=None):
        super().__init__(parent)
        self._explainer = explainer
        self._text = doubt_text

    def run(self):
        try:
            answer = self._explainer.explain_doubt(self._text)
            self.result_ready.emit(answer)
        except Exception as exc:
            self.error.emit(str(exc))


class LLMExamWorker(QThread):
    """Calls AIExplainer.explain_exam() in a background thread."""

    result_ready = Signal(str)
    error        = Signal(str)

    def __init__(self, explainer, paragraph_text: str, parent=None):
        super().__init__(parent)
        self._explainer = explainer
        self._text = paragraph_text

    def run(self):
        try:
            bullets = self._explainer.explain_exam(self._text)
            self.result_ready.emit(bullets)
        except Exception as exc:
            self.error.emit(str(exc))


# ── GUI Explanation Player ───────────────────────────────────────────────────

class GUIExplanationPlayer(QObject):
    """
    Orchestrates the full explanation lifecycle:
      1. Sends paragraph to LLM (background thread)
      2. Receives explanation text
      3. Splits into spoken chunks
      4. Drives AudioController to speak each chunk
      5. Supports pause / resume / stop / interrupt-for-doubt

    Signals
    -------
    status_changed(str)  : "thinking" | "speaking" | "paused" | "idle" | "error"
    chunk_spoken(int)    : index of chunk just spoken (for progress bar)
    all_done()           : full explanation finished
    doubt_answered(str)  : doubt explanation text ready
    exam_ready(str)      : exam bullet points ready
    """

    status_changed = Signal(str)
    chunk_spoken   = Signal(int)
    all_done       = Signal()
    explanation_ready = Signal(str, int)
    doubt_answered = Signal(str)
    exam_ready     = Signal(str)
    error_occurred = Signal(str)

    def __init__(self, explainer, speaker=None, parent=None):
        super().__init__(parent)
        self._explainer = explainer

        self._audio = AudioController(rate=165)
        self._audio.on_chunk_done = self._on_chunk_done
        self._audio.on_all_done   = self._on_all_done

        self._state: StateManager | None = None
        self._para_index: int = -1
        self._explanation_text: str = ""
        self._chunks: list[str] = []
        self._chunk_cursor: int = 0

        self._llm_worker: LLMWorker | None = None
        self._doubt_worker: LLMDoubtWorker | None = None
        self._exam_worker: LLMExamWorker | None = None
        self._active_workers: set[QThread] = set()

        self._paused = False
        self._interrupted = False

    # ── Main explanation flow ────────────────────────────────────────────

    def start(self, explanation_text: str | None, state: StateManager, para_index: int):
        """
        Begin explanation.
        If explanation_text is None or empty, fetch it from the LLM first.
        If it's already cached, go straight to TTS.
        """
        self._state = state
        self._para_index = para_index
        self._paused = False
        self._interrupted = False

        if explanation_text:
            self._explanation_text = explanation_text
            self._load_and_speak()
        # else: caller should pass pre-fetched text; LLM fetch done in fetch_explanation()

    def fetch_explanation(self, paragraph_text: str):
        """Kick off background LLM call. Emits status 'thinking'."""
        self.status_changed.emit("thinking")
        worker = LLMWorker(self._explainer, paragraph_text, parent=self)
        worker.result_ready.connect(self._on_explanation_ready)
        worker.error.connect(self._on_error)
        self._llm_worker = worker
        self._track_worker(worker)
        worker.start()

    def play_next(self):
        """Speak the next chunk (called externally to advance)."""
        self._audio.speak_next()

    def count_chunks_for(self, text: str) -> int:
        return len(self._split_to_chunks(text))

    def pause(self):
        self._paused = True
        self._audio.pause()
        self.status_changed.emit("paused")
        if self._state and self._para_index >= 0:
            self._state.set_resume_sentence(self._para_index, self._chunk_cursor)

    def resume(self):
        if self._paused or self._interrupted:
            self._paused = False
            self._interrupted = False
            self._audio.resume()
            self.status_changed.emit("speaking")

    def stop(self):
        self._audio.stop()
        self._chunk_cursor = 0
        self.status_changed.emit("idle")

    def shutdown(self, wait_ms: int | None = None):
        """Stop audio and wait for running workers to finish."""
        self.stop()
        for worker in list(self._active_workers):
            if worker.isRunning():
                if wait_ms is None:
                    worker.wait()
                else:
                    worker.wait(wait_ms)

    # ── Doubt handling ───────────────────────────────────────────────────

    def ask_doubt(self, doubt_text: str):
        """Interrupt playback and get a doubt explanation."""
        self.pause()
        self._interrupted = True
        self.status_changed.emit("thinking")

        worker = LLMDoubtWorker(self._explainer, doubt_text, parent=self)
        worker.result_ready.connect(self._on_doubt_ready)
        worker.error.connect(self._on_error)
        self._doubt_worker = worker
        self._track_worker(worker)
        worker.start()

    # ── Exam mode ────────────────────────────────────────────────────────

    def fetch_exam(self, paragraph_text: str):
        self.status_changed.emit("thinking")
        worker = LLMExamWorker(self._explainer, paragraph_text, parent=self)
        worker.result_ready.connect(self._on_exam_ready)
        worker.error.connect(self._on_error)
        self._exam_worker = worker
        self._track_worker(worker)
        worker.start()

    # ── Internal helpers ─────────────────────────────────────────────────

    def _load_and_speak(self):
        resume_at = 0
        if self._state and self._para_index >= 0:
            resume_at = self._state.get_resume_sentence(self._para_index)

        self._chunks = self._split_to_chunks(self._explanation_text)
        self._chunk_cursor = resume_at
        remaining = self._chunks[self._chunk_cursor:]

        if not remaining:
            self.all_done.emit()
            self.status_changed.emit("idle")
            return

        self._audio.enqueue(remaining)
        self.status_changed.emit("speaking")
        self._audio.speak_next()

    def _split_to_chunks(self, text: str, sentences_per_chunk: int = 2) -> list[str]:
        sentences = [s.strip() for s in text.split(".") if s.strip()]
        chunks, group = [], []
        for sentence in sentences:
            group.append(sentence)
            if len(group) >= sentences_per_chunk:
                chunks.append(". ".join(group) + ".")
                group = []
        if group:
            chunks.append(". ".join(group) + ".")
        return chunks

    # ── Slots ────────────────────────────────────────────────────────────

    def _on_explanation_ready(self, text: str):
        self._explanation_text = text
        self.explanation_ready.emit(text, len(self._split_to_chunks(text)))
        self._load_and_speak()

    def _on_chunk_done(self):
        self._chunk_cursor += 1
        self.chunk_spoken.emit(self._chunk_cursor)
        if self._state and self._para_index >= 0:
            self._state.set_resume_sentence(self._para_index, self._chunk_cursor)

    def _on_all_done(self):
        self.all_done.emit()
        self.status_changed.emit("idle")

    def _on_doubt_ready(self, text: str):
        self.doubt_answered.emit(text)
        # Speak the doubt answer, then wait for resume() call from UI
        self._audio.enqueue([text])
        self._audio.speak_next()

    def _on_exam_ready(self, text: str):
        self.exam_ready.emit(text)
        self.status_changed.emit("idle")

    def _on_error(self, message: str):
        self.error_occurred.emit(message)
        self.status_changed.emit("error")

    def _track_worker(self, worker: QThread):
        self._active_workers.add(worker)
        worker.finished.connect(lambda w=worker: self._on_worker_finished(w))

    def _on_worker_finished(self, worker: QThread):
        self._active_workers.discard(worker)
        if worker is self._llm_worker:
            self._llm_worker = None
        if worker is self._doubt_worker:
            self._doubt_worker = None
        if worker is self._exam_worker:
            self._exam_worker = None
        worker.deleteLater()
