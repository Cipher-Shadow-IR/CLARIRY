# study_engine/core/event_bus.py
# ─────────────────────────────
# Lightweight Qt-signal-compatible event bus.
# UI components subscribe to named events; engine components emit them.

from PySide6.QtCore import QObject, Signal


class EventBus(QObject):
    """
    Singleton-style event bus for CLARIRY.

    Usage:
        bus = EventBus.instance()
        bus.tts_finished.connect(my_slot)
        bus.tts_finished.emit()
    """

    # ── TTS / Playback ──────────────────────────────────────────
    tts_started   = Signal()            # spoken chunk started
    tts_finished  = Signal()            # one spoken chunk done
    tts_all_done  = Signal()            # entire explanation finished

    # ── Explanation lifecycle ────────────────────────────────────
    explanation_ready  = Signal(str)    # (explanation_text)
    explanation_done   = Signal()
    doubt_answered     = Signal(str)    # (doubt_answer_text)
    exam_ready         = Signal(str)    # (exam_bullet_text)

    # ── Navigation ───────────────────────────────────────────────
    paragraph_changed  = Signal(int)    # (new_index)

    # ── Status messages ──────────────────────────────────────────
    status_update      = Signal(str)    # ("Thinking…" / "Speaking" / etc.)
    error_occurred     = Signal(str)    # (error_message)

    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
