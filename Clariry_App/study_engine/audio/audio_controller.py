# study_engine/audio/audio_controller.py
# ────────────────────────────────────────
# Thread-safe TTS wrapper using QThread.
# Speaks one text chunk without blocking the Qt event loop.

import pyttsx3
from PySide6.QtCore import QThread, Signal


class TTSWorker(QThread):
    """
    Runs pyttsx3 speech synthesis in a background thread.
    Uses QThread's built-in `finished` signal when done.
    """

    error    = Signal(str)

    def __init__(self, text: str, rate: int = 165, parent=None):
        super().__init__(parent)
        self._text = text
        self._rate = rate

    def run(self):
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", self._rate)
            # Pick a clearer voice if available
            voices = engine.getProperty("voices")
            if voices:
                # Prefer English voices
                eng = [v for v in voices if "en" in v.id.lower()]
                if eng:
                    engine.setProperty("voice", eng[0].id)
            engine.say(self._text)
            engine.runAndWait()
            engine.stop()
        except Exception as exc:
            self.error.emit(str(exc))


class AudioController:
    """
    Manages a queue of text chunks and speaks them one at a time
    using TTSWorker threads. Supports pause, resume, and stop.
    """

    def __init__(self, rate: int = 165):
        self._rate = rate
        self._worker: TTSWorker | None = None
        self._queue: list[str] = []
        self._paused = False
        self._stopped = False

        # Callbacks — set by GUIExplanationPlayer
        self.on_chunk_done = None   # called after each chunk
        self.on_all_done   = None   # called when queue is empty

    # ── Control ───────────────────────────────────────────────────────

    def speak_next(self):
        """Speak the next chunk in the queue if not paused/stopped."""
        if self._paused or self._stopped:
            return
        if self._worker and self._worker.isRunning():
            return
        if not self._queue:
            if callable(self.on_all_done):
                self.on_all_done()
            return

        chunk = self._queue.pop(0)
        self._worker = TTSWorker(chunk, rate=self._rate)
        self._worker.finished.connect(self._on_worker_done)
        self._worker.start()

    def enqueue(self, chunks: list[str]):
        """Load a list of text chunks. Replaces any existing queue."""
        self._queue = list(chunks)
        self._paused = False
        self._stopped = False

    def pause(self):
        self._paused = True
        # We can't stop the current spoken chunk mid-word,
        # but next chunk won't start.

    def resume(self):
        if self._paused:
            self._paused = False
            if not (self._worker and self._worker.isRunning()):
                self.speak_next()

    def stop(self):
        self._stopped = True
        self._paused = False
        self._queue.clear()
        if self._worker and self._worker.isRunning():
            self._worker.wait()
        self._worker = None

    def is_idle(self) -> bool:
        return not self._queue and (
            self._worker is None or not self._worker.isRunning()
        )

    # ── Internal ──────────────────────────────────────────────────────

    def _on_worker_done(self):
        self._worker = None
        if callable(self.on_chunk_done):
            self.on_chunk_done()
        self.speak_next()
