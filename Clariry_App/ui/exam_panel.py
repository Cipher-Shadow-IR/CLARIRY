# ui/exam_panel.py
# ─────────────────
# Exam mode panel — shows bullet points generated for the current paragraph.

from __future__ import annotations
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QPushButton, QApplication,
)
from PySide6.QtCore import Qt


class ExamPanel(QWidget):
    """
    Replaces the center paragraph view content with exam bullet points.
    Displayed inside the main window's center panel.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Header row
        header = QHBoxLayout()
        title = QLabel("📘  EXAM NOTES")
        title.setStyleSheet(
            "font-size: 14px; font-weight: 700; color: #a78bfa; "
            "letter-spacing: 1px;"
        )

        self.copy_btn = QPushButton("⎘  Copy")
        self.copy_btn.setFixedWidth(90)
        self.copy_btn.setStyleSheet(
            "background: #312e81; color: #c7d2fe; border: 1px solid #3730a3; "
            "border-radius: 6px; padding: 4px 10px; font-size: 12px;"
        )
        self.copy_btn.clicked.connect(self._copy_to_clipboard)

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.copy_btn)
        layout.addLayout(header)

        # Bullet text area
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setStyleSheet(
            "background-color: #0f0c29; border: 1px solid #3730a3; "
            "border-radius: 8px; padding: 16px; color: #c7d2fe; "
            "font-size: 13px; line-height: 1.8;"
        )
        layout.addWidget(self.text_area)

    # ── Public API ───────────────────────────────────────────────────────

    def show_bullets(self, bullets: str):
        self.text_area.setPlainText(bullets)

    def show_loading(self):
        self.text_area.setPlainText("⟳  Generating exam notes…")

    def clear(self):
        self.text_area.clear()

    # ── Internal ─────────────────────────────────────────────────────────

    def _copy_to_clipboard(self):
        text = self.text_area.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            self.copy_btn.setText("✓ Copied!")
            from PySide6.QtCore import QTimer
            QTimer.singleShot(1800, lambda: self.copy_btn.setText("⎘  Copy"))
