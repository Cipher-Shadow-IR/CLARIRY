# ui/doubt_dialog.py
# ───────────────────
# Modal dialog for the student to type a doubt.
# Launches a background LLM call and shows the answer in an output box.

from __future__ import annotations
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QPushButton, QSizePolicy,
)
from PySide6.QtCore import Qt, QThread, Signal


class DoubtWorker(QThread):
    """Background thread for doubt explanation via AIExplainer."""
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


class DoubtDialog(QDialog):
    """
    Modal dialogue:
    ┌───────────────────────────────────────────┐
    │  ❓ ASK YOUR DOUBT                        │
    │  ─────────────────────────────────────    │
    │  [Input box — type the confusing part]    │
    │  [ Ask Tutor ]                            │
    │  ─────────────────────────────────────    │
    │  Tutor's answer appears here…             │
    │  [ Close ]   [ Resume Explanation ]       │
    └───────────────────────────────────────────┘
    """

    resume_requested = Signal()

    def __init__(self, explainer, parent=None):
        super().__init__(parent)
        self._explainer = explainer
        self._worker: DoubtWorker | None = None

        self.setWindowTitle("Ask Your Doubt")
        self.setMinimumWidth(520)
        self.setMinimumHeight(420)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        # Title
        title = QLabel("❓  What didn't you understand?")
        title.setStyleSheet("font-size: 16px; font-weight: 700; color: #00c8ff;")
        layout.addWidget(title)

        sub = QLabel("Type or paste the confusing part from the paragraph:")
        sub.setStyleSheet("color: #94a3b8; font-size: 12px;")
        layout.addWidget(sub)

        # Input box
        self.input_box = QTextEdit()
        self.input_box.setPlaceholderText("e.g. 'I didn't understand what a semaphore does…'")
        self.input_box.setFixedHeight(90)
        self.input_box.setStyleSheet(
            "border: 1px solid #00c8ff44; border-radius: 8px; padding: 10px;"
        )
        layout.addWidget(self.input_box)

        # Ask button
        self.ask_btn = QPushButton("⟳  Ask Tutor")
        self.ask_btn.setObjectName("btn_primary")
        self.ask_btn.clicked.connect(self._ask)
        layout.addWidget(self.ask_btn)

        # Divider label
        self.answer_label = QLabel("Tutor's answer will appear below:")
        self.answer_label.setStyleSheet("color: #4a5568; font-size: 11px;")
        layout.addWidget(self.answer_label)

        # Answer box
        self.answer_box = QTextEdit()
        self.answer_box.setReadOnly(True)
        self.answer_box.setPlaceholderText("…")
        self.answer_box.setStyleSheet(
            "border: 1px solid #1e2d3d; border-radius: 8px; "
            "background: #0d1117; padding: 12px; color: #a7f3d0;"
        )
        layout.addWidget(self.answer_box)

        # Footer buttons
        footer = QHBoxLayout()
        self.close_btn = QPushButton("✕  Close")
        self.close_btn.clicked.connect(self.reject)

        self.resume_btn = QPushButton("▶  Resume Explanation")
        self.resume_btn.setObjectName("btn_primary")
        self.resume_btn.setEnabled(False)
        self.resume_btn.clicked.connect(self._resume)

        footer.addWidget(self.close_btn)
        footer.addStretch()
        footer.addWidget(self.resume_btn)
        layout.addLayout(footer)

    # ── Logic ─────────────────────────────────────────────────────────────

    def _ask(self):
        text = self.input_box.toPlainText().strip()
        if not text:
            self.input_box.setStyleSheet(
                "border: 1px solid #f87171; border-radius: 8px; padding: 10px;"
            )
            return

        self.ask_btn.setEnabled(False)
        self.ask_btn.setText("⟳  Asking…")
        self.answer_box.setPlainText("Thinking…")

        self._worker = DoubtWorker(self._explainer, text, parent=self)
        self._worker.result_ready.connect(self._on_answer)
        self._worker.error.connect(self._on_error)
        self._worker.finished.connect(self._on_worker_finished)
        self._worker.start()

    def _on_answer(self, text: str):
        self.answer_box.setPlainText(text)
        self.ask_btn.setEnabled(True)
        self.ask_btn.setText("⟳  Ask Again")
        self.resume_btn.setEnabled(True)

    def _on_error(self, msg: str):
        self.answer_box.setPlainText(f"[Error: {msg}]")
        self.ask_btn.setEnabled(True)
        self.ask_btn.setText("⟳  Ask Tutor")

    def _resume(self):
        self.resume_requested.emit()
        self.accept()

    def _on_worker_finished(self):
        if self._worker:
            self._worker.deleteLater()
            self._worker = None

    def closeEvent(self, event):
        if self._worker and self._worker.isRunning():
            self._worker.wait()
        super().closeEvent(event)
