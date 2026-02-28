# ui/main_window.py
# ──────────────────
# CLARIRY — Main Window
# Premium dark-mode desktop UI tying together all engine + UI components.

from __future__ import annotations
import os
import sys

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout, QSplitter,
    QLabel, QFileDialog, QPushButton, QStackedWidget,
    QGraphicsDropShadowEffect, QSplitter,
)
from PySide6.QtCore import Qt, QTimer, Property, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QShortcut, QKeySequence, QColor, QIcon, QPixmap

from ui.theme import DARK_THEME
from ui.paragraph_list import ParagraphListWidget
from ui.pdf_view import ParagraphView
from ui.controls import ControlsPanel
from ui.doubt_dialog import DoubtDialog
from ui.exam_panel import ExamPanel

from study_engine.paragraph_store import ParaStore
from study_engine.state_manager import StateManager
from study_engine.explainer import Explainer
from study_engine.gui_player import GUIExplanationPlayer
from study_engine.persistence.progress_store import ProgressStore


class ToastNotification(QWidget):
    """Premium floating notification."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("toast_notif")
        self.setFixedWidth(280)
        self.setFixedHeight(50)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 15, 0)
        
        self.label = QLabel("")
        self.label.setObjectName("toast_msg")
        layout.addWidget(self.label)
        
        # Shadow (Qt uses QGraphicsDropShadowEffect instead of CSS box-shadow)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 120))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        
        self.hide()
        
        self._opacity_anim = QPropertyAnimation(self, b"windowOpacity")
        self._pos_anim = QPropertyAnimation(self, b"pos")

    def show_message(self, text: str, duration=3000):
        self.label.setText(text)
        
        parent_rect = self.parent().rect()
        target_x = (parent_rect.width() - self.width()) // 2
        target_y = 80 # Below header
        
        self.move(target_x, target_y - 20)
        self.show()
        
        # Slide in
        self._pos_anim.setDuration(400)
        self._pos_anim.setStartValue(self.pos())
        self._pos_anim.setEndValue(QPoint(target_x, target_y))
        self._pos_anim.setEasingCurve(QEasingCurve.OutCubic)
        self._pos_anim.start()
        
        QTimer.singleShot(duration, self._fade_out)

    def _fade_out(self):
        self.hide()


class MainWindow(QMainWindow):
    """
    CLARIRY main window.
    Premium 'Universe Teacher' Edition.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CLARIRY — Universe Teacher")
        self.resize(1400, 900)
        self.setMinimumSize(1100, 800)

        # Set Window Icon
        icon_path = os.path.join("public", "assets", "CLARIRY_LOGO.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Apply global stylesheet
        QApplication.instance().setStyleSheet(DARK_THEME)

        # ── Engine state ─────────────────────────────────────────────────
        self._store: ParaStore | None = None
        self._state: StateManager | None = None
        self._explainer = Explainer()
        self._player = GUIExplanationPlayer(self._explainer)
        self._progress = ProgressStore()
        self._current_index: int = -1
        self._is_playing: bool = False
        self._exam_mode: bool = False
        self._auto_advance: bool = True
        self._explanation_cache: dict[int, str] = {}
        self._chunk_total: int = 0
        self._programmatic_selection: bool = False

        # ── Connect player signals ────────────────────────────────────────
        self._player.status_changed.connect(self._on_status_changed)
        self._player.chunk_spoken.connect(self._on_chunk_spoken)
        self._player.all_done.connect(self._on_all_done)
        self._player.explanation_ready.connect(self._on_explanation_ready)
        self._player.doubt_answered.connect(self._on_doubt_answered)
        self._player.exam_ready.connect(self._on_exam_ready)
        self._player.error_occurred.connect(self._on_engine_error)

        # ── Build UI ──────────────────────────────────────────────────────
        self._build_ui()
        self._setup_shortcuts()
        
        self._toast = ToastNotification(self)

    # ═════════════════════════════════════════════════════════════════════
    # UI Construction
    # ═════════════════════════════════════════════════════════════════════

    def _build_ui(self):
        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)

        main_layout = QVBoxLayout(root)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = self._build_header()
        main_layout.addWidget(header)

        # 3-Pane Body
        self._splitter = QSplitter(Qt.Horizontal)
        self._splitter.setChildrenCollapsible(False)
        self._splitter.setHandleWidth(1)

        self._sidebar = self._build_sidebar()
        self._splitter.addWidget(self._sidebar)

        self._center_stack = QStackedWidget()
        self._para_view = ParagraphView()
        self._exam_panel = ExamPanel()
        self._center_stack.addWidget(self._para_view)
        self._center_stack.addWidget(self._exam_panel)
        
        center_container = QWidget()
        center_container.setObjectName("center_panel")
        cl = QVBoxLayout(center_container)
        cl.setContentsMargins(10, 10, 10, 10)
        cl.addWidget(self._center_stack)
        self._splitter.addWidget(center_container)

        self._controls = ControlsPanel()
        self._splitter.addWidget(self._controls)
        self._splitter.setStretchFactor(0, 1)
        self._splitter.setStretchFactor(1, 4)
        self._splitter.setStretchFactor(2, 1)

        main_layout.addWidget(self._splitter)

        # Wire control signals
        self._controls.play_clicked.connect(self.toggle_play)
        self._controls.doubt_clicked.connect(self.open_doubt_dialog)
        self._controls.exam_clicked.connect(self.toggle_exam_mode)

    def _build_header(self) -> QWidget:
        header = QWidget()
        header.setObjectName("header")
        header.setFixedHeight(80)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(24, 0, 24, 0)

        # Brand Image (Brand mark + Name)
        self.brand_label = QLabel()
        brand_path = os.path.join("public", "assets", "CLARIRY_Brand.png")
        if os.path.exists(brand_path):
            pix = QPixmap(brand_path).scaledToHeight(40, Qt.SmoothTransformation)
            self.brand_label.setPixmap(pix)
        else:
            self.brand_label.setText("CLARIRY")
            self.brand_label.setObjectName("app_title")

        # File status
        self._file_label = QLabel("Orbiting your notes...")
        self._file_label.setObjectName("file_label")
        self._file_label.setStyleSheet("color: #a5b4fc; font-weight: 600; margin-left: 20px;")

        open_btn = QPushButton("📂  TRANSVERSE NEW GALAXY")
        open_btn.setFixedWidth(240)
        open_btn.setObjectName("btn_primary")
        open_btn.clicked.connect(self._open_file)

        layout.addWidget(self.brand_label)
        layout.addWidget(self._file_label)
        layout.addStretch()
        layout.addSpacing(20)
        layout.addWidget(open_btn)

        return header

    def _build_sidebar(self) -> QWidget:
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setMinimumWidth(260)
        sidebar.setMaximumWidth(340)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 12, 0, 12)
        layout.setSpacing(4)

        col_title = QLabel("  STUDY GUIDE")
        col_title.setObjectName("section_title")
        layout.addWidget(col_title)

        self._para_list = ParagraphListWidget()
        self._para_list.paragraph_clicked.connect(self._on_paragraph_clicked)
        layout.addWidget(self._para_list)

        return sidebar

    # ═════════════════════════════════════════════════════════════════════
    # Document Loading
    # ═════════════════════════════════════════════════════════════════════

    def _open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Study Document",
            "",
            "Study Files (*.pdf *.txt);;PDF Files (*.pdf);;Text Files (*.txt)",
        )
        if not path:
            return
        self._load_document(path)

    def _load_document(self, path: str):
        try:
            self._store = ParaStore(path)
        except Exception as exc:
            self._controls.set_status("error")
            self._toast.show_message("Oops! Couldn't load that file.")
            return

        total = self._store.total_para()
        if total == 0:
            return

        self._state = StateManager(total)
        self._explanation_cache.clear()
        self._chunk_total = 0

        # Load persisted progress
        saved = self._progress.load(path)
        if saved:
            self._state._resume_points = self._progress.get_resume_points()
            start_index = self._progress.get_last_paragraph()
        else:
            start_index = 0

        # Populate list
        self._para_list.load_paragraphs(self._store.all_paras())

        # Mark previously explained paragraphs
        for idx in self._progress.get_explained():
            self._para_list.mark_explained(idx)

        # Update header
        fname = os.path.basename(path)
        self._file_label.setText(f"📄 {fname}  ({total} sections)")
        self._para_view.load_document(path, self._store.is_pdf)

        # Jump to saved position
        self._para_list.jump_to(start_index)
        self._controls.set_status("idle")
        self._controls.reset_progress()
        self._toast.show_message("Great! Let's get started.")

    # ═════════════════════════════════════════════════════════════════════
    # Paragraph Selection
    # ═════════════════════════════════════════════════════════════════════

    def _on_paragraph_clicked(self, index: int):
        if not self._store:
            return

        # Stop any ongoing playback
        if self._is_playing and not self._programmatic_selection:
            self._player.stop()
            self._is_playing = False

        self._current_index = index

        paragraph = self._store.get_para(index)
        if not paragraph:
            return

        # Show paragraph text or real PDF page with highlight
        source = self._store.get_source(index)
        self._para_view.show_paragraph(index, paragraph, source)

        # Switch back to paragraph view if in exam mode display
        if not self._exam_mode:
            self._center_stack.setCurrentIndex(0)

        self._controls.set_status("idle")
        self._controls.reset_progress()
        self._exam_mode = False
        self._controls.exam_btn.setChecked(False)

    # ═════════════════════════════════════════════════════════════════════
    # Playback
    # ═════════════════════════════════════════════════════════════════════

    def toggle_play(self):
        if self._current_index < 0 or not self._store:
            self._toast.show_message("Select a paragraph first!")
            return

        if not self._is_playing:
            self._start_playback()
        else:
            self._pause_playback()

    def _start_playback(self):
        self._is_playing = True

        # Check explanation cache
        cached = self._explanation_cache.get(self._current_index)
        if cached:
            self._chunk_total = self._player.count_chunks_for(cached)
            self._player.start(cached, self._state, self._current_index)
        else:
            # Need to fetch from LLM first
            paragraph = self._store.get_para(self._current_index)
            # NO LONGER CALLING show_thinking() to avoid vanishing PDF
            self._player.fetch_explanation(paragraph)

    def _pause_playback(self):
        self._is_playing = False
        self._player.pause()

    # ═════════════════════════════════════════════════════════════════════
    # Doubt Flow
    # ═════════════════════════════════════════════════════════════════════

    def open_doubt_dialog(self):
        if self._current_index < 0:
            return
        # Pause first
        if self._is_playing:
            self._player.pause()
            self._is_playing = False

        dialog = DoubtDialog(self._explainer, parent=self)
        dialog.resume_requested.connect(self._resume_after_doubt)
        dialog.exec()

    def _resume_after_doubt(self):
        self._is_playing = True
        self._player.resume()

    # ═════════════════════════════════════════════════════════════════════
    # Exam Mode
    # ═════════════════════════════════════════════════════════════════════

    def toggle_exam_mode(self):
        if self._current_index < 0 or not self._store:
            self._controls.exam_btn.setChecked(False)
            return

        self._exam_mode = not self._exam_mode

        if self._exam_mode:
            # Stop playback
            if self._is_playing:
                self._player.stop()
                self._is_playing = False

            self._center_stack.setCurrentIndex(1)   # show exam panel
            self._exam_panel.show_loading()
            paragraph = self._store.get_para(self._current_index)
            self._player.fetch_exam(paragraph)
            self._toast.show_message("Summarizing for you...")
        else:
            self._center_stack.setCurrentIndex(0)   # back to para view
            self._controls.exam_btn.setChecked(False)

    # ═════════════════════════════════════════════════════════════════════
    # Player Signal Handlers
    # ═════════════════════════════════════════════════════════════════════

    def _on_status_changed(self, state: str):
        self._controls.set_status(state)
        
        if state == "thinking":
            self._toast.show_message("Give me a second to think... 🤔")
        elif state == "speaking":
            self._toast.show_message("Here's how I see it! 👇")

    def _on_chunk_spoken(self, chunk_index: int):
        if self._chunk_total > 0:
            self._controls.set_progress(chunk_index, self._chunk_total)

    def _on_explanation_ready(self, text: str, chunk_total: int):
        if self._current_index >= 0:
            self._explanation_cache[self._current_index] = text
        self._chunk_total = chunk_total
        self._controls.set_progress(0, max(1, chunk_total))

    def _on_all_done(self):
        self._is_playing = False
        self._controls.set_status("idle")
        self._controls.set_progress(100, 100)

        # Mark paragraph as explained
        if self._current_index >= 0:
            self._para_list.mark_explained(self._current_index)
            self._save_progress()

        # Auto-advance
        if self._auto_advance and self._store and self._state:
            next_idx = self._current_index + 1
            if next_idx < self._store.total_para():
                def _advance_and_continue():
                    self._programmatic_selection = True
                    self._para_list.jump_to(next_idx)
                    self._programmatic_selection = False
                    self._start_playback()
                QTimer.singleShot(1200, _advance_and_continue)

    def _on_doubt_answered(self, text: str):
        # Already spoken via audio; just log
        pass

    def _on_exam_ready(self, bullets: str):
        self._exam_panel.show_bullets(bullets)
        self._toast.show_message("Ready for the exam! ✅")

    def _on_engine_error(self, message: str):
        self._controls.set_status("error")
        self._is_playing = False
        self._toast.show_message("Something went wrong. Let's try again?")

    # ═════════════════════════════════════════════════════════════════════
    # Keyboard Shortcuts
    # ═════════════════════════════════════════════════════════════════════

    def _setup_shortcuts(self):
        QShortcut(QKeySequence(Qt.Key_Space),  self, activated=self.toggle_play)
        QShortcut(QKeySequence(Qt.Key_Up),     self, activated=self._nav_previous)
        QShortcut(QKeySequence(Qt.Key_Down),   self, activated=self._nav_next)
        QShortcut(QKeySequence("D"),           self, activated=self.open_doubt_dialog)
        QShortcut(QKeySequence("E"),           self, activated=self.toggle_exam_mode)

    def _nav_previous(self):
        cur = self._para_list.currentRow()
        if cur > 0:
            self._para_list.setCurrentRow(cur - 1)

    def _nav_next(self):
        cur = self._para_list.currentRow()
        if cur < self._para_list.count() - 1:
            self._para_list.setCurrentRow(cur + 1)

    # ═════════════════════════════════════════════════════════════════════
    # Persistence
    # ═════════════════════════════════════════════════════════════════════

    def _save_progress(self):
        if not self._store or not self._state:
            return
        explained = [
            i for i in range(self._store.total_para())
            if i in self._state._resume_points or
            (self._para_list.item(i) and "✓" in (self._para_list.item(i).text() or ""))
        ]
        self._progress.save(
            document_path=self._store.file_path,
            last_paragraph=self._current_index,
            resume_points=self._state._resume_points,
            explained=explained,
        )

    def closeEvent(self, event):
        self._save_progress()
        self._player.shutdown()
        super().closeEvent(event)


# ── Standalone runner ────────────────────────────────────────────────────────

def run():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()
