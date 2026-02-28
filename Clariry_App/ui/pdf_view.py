from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QImage, QPainter, QPen, QPixmap, QTextCharFormat, QTextCursor
from PySide6.QtWidgets import QLabel, QScrollArea, QStackedWidget, QTextEdit, QVBoxLayout, QWidget


class ParagraphView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("paragraph_view_container")

        self._is_pdf = False
        self._pdf_doc = None
        self._zoom = 1.6

        self._stack = QStackedWidget(self)

        self._text_view = QTextEdit()
        self._text_view.setReadOnly(True)
        self._text_view.setObjectName("paragraph_view")
        self._text_view.setFrameShape(QTextEdit.NoFrame)
        self._text_view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self._text_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        font = QFont("Segoe UI", 13)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 0.2)
        self._text_view.setFont(font)

        self._pdf_label = QLabel()
        self._pdf_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self._pdf_label.setText("PDF preview unavailable.")
        self._pdf_label.setStyleSheet("color: #64748b; padding: 24px;")

        self._pdf_scroll = QScrollArea()
        self._pdf_scroll.setWidgetResizable(True)
        self._pdf_scroll.setWidget(self._pdf_label)
        self._pdf_scroll.setFrameShape(QScrollArea.NoFrame)

        self._stack.addWidget(self._text_view)
        self._stack.addWidget(self._pdf_scroll)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._stack)

        self._show_placeholder()

    def load_document(self, path: str, is_pdf: bool):
        if self._pdf_doc is not None:
            try:
                self._pdf_doc.close()
            except Exception:
                pass
        self._is_pdf = is_pdf
        self._pdf_doc = None
        if not is_pdf:
            self._stack.setCurrentWidget(self._text_view)
            return

        try:
            import fitz
            self._pdf_doc = fitz.open(path)
        except Exception:
            self._pdf_doc = None
            self._stack.setCurrentWidget(self._text_view)

    def show_paragraph(self, index: int, text: str, source=None):
        if self._is_pdf and self._pdf_doc and source and source.page_index is not None:
            rendered = self._render_pdf_with_highlight(source.page_index, source.rect)
            if rendered is not None:
                self._pdf_label.setPixmap(rendered)
                self._stack.setCurrentWidget(self._pdf_scroll)
                return
        self._show_text_paragraph(index, text)

    def show_exam(self, index: int, bullets: str):
        self._stack.setCurrentWidget(self._text_view)
        self._text_view.clear()
        cursor = self._text_view.textCursor()

        header_fmt = QTextCharFormat()
        header_fmt.setForeground(QColor("#a5b4fc"))
        header_fmt.setFontPointSize(12)
        header_fmt.setFontWeight(QFont.Weight.Bold)
        cursor.setCharFormat(header_fmt)
        cursor.insertText(f"EXAM NOTES — PARAGRAPH {index + 1}\n\n")

        bullet_fmt = QTextCharFormat()
        bullet_fmt.setForeground(QColor("#e2e8f0"))
        bullet_fmt.setFontPointSize(13)
        cursor.setCharFormat(bullet_fmt)
        cursor.insertText(bullets)

        self._text_view.setTextCursor(cursor)
        self._text_view.moveCursor(QTextCursor.Start)

    def _show_text_paragraph(self, index: int, text: str):
        self._stack.setCurrentWidget(self._text_view)
        self._text_view.clear()
        cursor = self._text_view.textCursor()

        header_fmt = QTextCharFormat()
        header_fmt.setForeground(QColor("#38bdf8"))
        header_fmt.setFontPointSize(12)
        header_fmt.setFontWeight(QFont.Weight.Bold)
        cursor.setCharFormat(header_fmt)
        cursor.insertText(f"PARAGRAPH {index + 1}\n\n")

        body_fmt = QTextCharFormat()
        body_fmt.setForeground(QColor("#f1f5f9"))
        body_fmt.setFontPointSize(14)
        cursor.setCharFormat(body_fmt)
        cursor.insertText(text)

        self._text_view.setTextCursor(cursor)
        self._text_view.moveCursor(QTextCursor.Start)

    def _render_pdf_with_highlight(self, page_index: int, rect):
        if not self._pdf_doc:
            return None
        try:
            import fitz
            page = self._pdf_doc.load_page(page_index)
            pix = page.get_pixmap(matrix=fitz.Matrix(self._zoom, self._zoom), alpha=False)
            image = QImage(
                pix.samples,
                pix.width,
                pix.height,
                pix.stride,
                QImage.Format_RGB888,
            ).copy()
            if rect:
                x0, y0, x1, y1 = rect
                sx = int(x0 * self._zoom)
                sy = int(y0 * self._zoom)
                sw = int((x1 - x0) * self._zoom)
                sh = int((y1 - y0) * self._zoom)
                painter = QPainter(image)
                painter.fillRect(sx, sy, sw, sh, QColor(0, 200, 255, 72))
                pen = QPen(QColor(56, 189, 248))
                pen.setWidth(3)
                painter.setPen(pen)
                painter.drawRect(sx, sy, sw, sh)
                painter.end()
            return QPixmap.fromImage(image)
        except Exception:
            return None

    def _show_placeholder(self):
        cursor = self._text_view.textCursor()
        fmt = QTextCharFormat()
        fmt.setForeground(QColor("#64748b"))
        fmt.setFontPointSize(15)
        fmt.setFontItalic(True)
        cursor.setCharFormat(fmt)
        cursor.insertText(
            "Hey! Select a paragraph from the sidebar\n"
            "to begin our study session together! 😊"
        )
        self._text_view.setTextCursor(cursor)
