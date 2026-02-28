# ui/controls.py
# ────────────────
# Right-side controls panel: play/pause, doubt, exam mode, auto-advance.

from __future__ import annotations
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QLabel, QProgressBar, QFrame, QCheckBox,
)
from PySide6.QtCore import Qt, Signal
from ui.theme import STATUS_COLORS


class ControlsPanel(QWidget):
    """
    Right-side panel with playback controls, status display,
    progress bar, and feature toggles.

    Signals
    -------
    play_clicked()
    doubt_clicked()
    exam_clicked()
    auto_advance_changed(bool)
    """

    play_clicked         = Signal()
    doubt_clicked        = Signal()
    exam_clicked         = Signal()
    auto_advance_changed = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("right_panel")
        self.setMinimumWidth(200)
        self.setMaximumWidth(260)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 16, 12, 16)
        layout.setSpacing(10)

        # ── Section: Status ──────────────────────────────────────────
        layout.addWidget(self._section_label("STATUS"))

        self.status_chip = QLabel("● Idle")
        self.status_chip.setObjectName("status_chip")
        self.status_chip.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_chip)

        # ── Progress bar ─────────────────────────────────────────────
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(6)
        layout.addWidget(self.progress_bar)

        layout.addWidget(self._divider())

        # ── Section: Playback ────────────────────────────────────────
        layout.addWidget(self._section_label("PLAYBACK"))

        self.play_btn = QPushButton("▶  Start")
        self.play_btn.setObjectName("btn_primary")
        self.play_btn.setToolTip("Space")
        self.play_btn.clicked.connect(self.play_clicked)
        layout.addWidget(self.play_btn)

        layout.addWidget(self._divider())

        # ── Section: Doubt ───────────────────────────────────────────
        layout.addWidget(self._section_label("ASK A DOUBT"))

        self.doubt_btn = QPushButton("❓  Interrupt & Ask")
        self.doubt_btn.setToolTip("D — pause and ask a doubt")
        self.doubt_btn.clicked.connect(self.doubt_clicked)
        layout.addWidget(self.doubt_btn)

        layout.addWidget(self._divider())

        # ── Section: Exam Mode ────────────────────────────────────────
        layout.addWidget(self._section_label("EXAM MODE"))

        self.exam_btn = QPushButton("📘  Show Exam Notes")
        self.exam_btn.setObjectName("btn_exam")
        self.exam_btn.setToolTip("E — generate exam bullet points")
        self.exam_btn.setCheckable(True)
        self.exam_btn.clicked.connect(self.exam_clicked)
        layout.addWidget(self.exam_btn)

        layout.addWidget(self._divider())

        # ── Section: Settings ─────────────────────────────────────────
        layout.addWidget(self._section_label("OPTIONS"))

        self.auto_advance_cb = QCheckBox("Auto-advance paragraphs")
        self.auto_advance_cb.setChecked(True)
        self.auto_advance_cb.setStyleSheet("color: #94a3b8; font-size: 12px;")
        self.auto_advance_cb.stateChanged.connect(
            lambda s: self.auto_advance_changed.emit(bool(s))
        )
        layout.addWidget(self.auto_advance_cb)

        layout.addStretch()

        # ── Keyboard hint ─────────────────────────────────────────────
        hint = QLabel(
            "<span style='color:#2d3748'>"
            "Space = play/pause<br>"
            "↑ ↓ = navigate<br>"
            "D = ask doubt<br>"
            "E = exam mode"
            "</span>"
        )
        hint.setTextFormat(Qt.RichText)
        hint.setWordWrap(True)
        hint.setStyleSheet("font-size: 11px; padding: 8px;")
        layout.addWidget(hint)

    # ── Public API ───────────────────────────────────────────────────────

    def set_status(self, state: str):
        """Update status chip. state ∈ {idle, thinking, speaking, paused, error}"""
        style, label = STATUS_COLORS.get(state, STATUS_COLORS["idle"])
        self.status_chip.setStyleSheet(
            f"font-size: 12px; font-weight: 600; padding: 4px 12px; "
            f"border-radius: 12px; {style}"
        )
        self.status_chip.setText(label)

        if state == "speaking":
            self.play_btn.setText("⏸  Pause")
            self.play_btn.setEnabled(True)
        elif state == "paused":
            self.play_btn.setText("▶  Resume")
            self.play_btn.setEnabled(True)
        elif state == "thinking":
            self.play_btn.setText("⟳  Generating...")
            self.play_btn.setEnabled(False)  # Disable while thinking to prevent double clicks
        else:
            self.play_btn.setText("▶  Start")
            self.play_btn.setEnabled(True)

    def set_progress(self, current: int, total: int):
        if total > 0:
            self.progress_bar.setValue(int(current / total * 100))
        else:
            self.progress_bar.setValue(0)

    def reset_progress(self):
        self.progress_bar.setValue(0)

    # ── Helpers ───────────────────────────────────────────────────────────

    def _section_label(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setObjectName("section_title")
        return lbl

    def _divider(self) -> QFrame:
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #1e2d3d;")
        return line
