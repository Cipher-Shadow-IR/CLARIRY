# ui/paragraph_list.py
# ─────────────────────
# Custom paragraph list widget with explained badges and smooth highlighting.

from __future__ import annotations
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor


class ParagraphListWidget(QListWidget):
    """
    Sidebar list of paragraph items.
    - Highlights the active paragraph in teal.
    - Shows ✓ badge for fully explained paragraphs.
    - Emits `paragraph_clicked(int)` on selection.
    """

    paragraph_clicked = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._explained: set[int] = set()
        self._labels: list[str] = []  # paragraph preview text
        self.setObjectName("paragraph_list")
        self.currentRowChanged.connect(self._on_row_changed)
        # No internal frame border — theme handles it
        self.setFrameShape(QListWidget.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    # ── Public API ───────────────────────────────────────────────────────

    def load_paragraphs(self, paragraphs: list[str]):
        """Populate the list from a list of paragraph strings."""
        self.clear()
        self._labels.clear()
        self._explained.clear()

        for i, para in enumerate(paragraphs):
            preview = para[:55].replace("\n", " ") + ("…" if len(para) > 55 else "")
            label = f"  {i + 1}. {preview}"
            self._labels.append(label)
            item = QListWidgetItem(label)
            item.setData(Qt.UserRole, i)
            item.setToolTip(para[:200])
            self.addItem(item)

    def mark_explained(self, index: int):
        """Add a ✓ badge to a paragraph item."""
        self._explained.add(index)
        item = self.item(index)
        if item:
            base = self._labels[index] if index < len(self._labels) else ""
            if "✓" not in item.text():
                item.setText(base + "  ✓")
                item.setForeground(QColor("#34d399"))

    def jump_to(self, index: int):
        """Programmatically select a paragraph."""
        if 0 <= index < self.count():
            self.setCurrentRow(index)
            self.scrollToItem(self.item(index))

    # ── Internal ─────────────────────────────────────────────────────────

    def _on_row_changed(self, row: int):
        if row >= 0:
            self.paragraph_clicked.emit(row)
