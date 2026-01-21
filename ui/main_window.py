import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QTextEdit,
    QFrame,
    QPushButton,
)
from PySide6.QtCore import (
    Qt,
    QTimer,
)
from PySide6.QtGui import QShortcut
from PySide6.QtGui import QKeySequence

# STUDY ENGINE IMPORTS

from study_engine.paragraph_store import ParaStore
from study_engine.state_manager import StateManager
from study_engine.explainer import Explainer
from study_engine.gui_player import GUIExplanationPlayer
from study_engine.tts_speaker import TTSSpeaker



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CLARIRY - YOUR TUTOR-FRIEND")
        self.resize(1200, 800)

        self.is_playing = False

        # -------- Engine Setup --------
        self.store = ParaStore("data/sample_text.txt")
        self.state = StateManager(self.store.total_para())
        self.explainer = Explainer()

        # -------- Explanation Playback --------
        speaker = TTSSpeaker()
        self.player = GUIExplanationPlayer(speaker)

        # Root container
        root = QWidget()
        self.setCentralWidget(root)

        # Main horizontal layout
        main_layout = QHBoxLayout()
        root.setLayout(main_layout)

        # Left panel — Paragraph list
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)

        self.paragraph_list = QListWidget()
        for i in range(self.store.total_para()):
            self.paragraph_list.addItem(f"Paragraph {i + 1}")

        left_layout.addWidget(QLabel("Paragraphs"))
        left_layout.addWidget(self.paragraph_list)

        self.paragraphs = [
            self.store.get_para(i)
            for i in range(self.store.total_para())
        ]

        self.paragraph_list.currentRowChanged.connect(
            self.on_paragraph_selected
        )

        # Center panel — Content view
        center_panel = QWidget()
        center_layout = QVBoxLayout()
        center_panel.setLayout(center_layout)

        title_label = QLabel("Current Paragraph")
        title_label.setStyleSheet("font-weight: bold; font-size: 16px;")

        self.content_box = QTextEdit()
        self.content_box.setReadOnly(True)
        self.content_box.setText("Select a paragraph to begin.")

        content_frame = QFrame()
        content_frame.setFrameShape(QFrame.StyledPanel)
        content_frame_layout = QVBoxLayout()
        content_frame.setLayout(content_frame_layout)
        content_frame_layout.addWidget(self.content_box)

        center_layout.addWidget(title_label)
        center_layout.addWidget(content_frame)

        # Right panel — Controls
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)

        controls_title = QLabel("Controls")
        controls_title.setStyleSheet("font-weight: bold; font-size: 14px;")

        self.play_button = QPushButton("▶ Play")
        self.exam_button = QPushButton("📘 Exam Mode")

        self.status_label = QLabel("Status: Paused")
        self.status_label.setStyleSheet("color: gray;")

        right_layout.addWidget(controls_title)
        right_layout.addWidget(self.play_button)
        right_layout.addWidget(self.exam_button)
        right_layout.addStretch()
        right_layout.addWidget(self.status_label)
        self.play_button.clicked.connect(self.toggle_play)

        # Add panels to main layout
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(center_panel, 3)
        main_layout.addWidget(right_panel, 1)

        self.setFocusPolicy(Qt.StrongFocus)

        # -------- Global Keyboard Shortcuts --------

        QShortcut(QKeySequence(Qt.Key_Space), self, activated=self.toggle_play)

        QShortcut(QKeySequence(Qt.Key_Up), self, activated=self.select_previous)
        QShortcut(QKeySequence(Qt.Key_Down), self, activated=self.select_next)

        QShortcut(QKeySequence(Qt.Key_Return), self, activated=self.explain_current)
        QShortcut(QKeySequence(Qt.Key_Enter), self, activated=self.explain_current)

        QShortcut(QKeySequence("E"), self, activated=self.enter_exam_mode)


    def on_paragraph_selected(self, index):
        if index < 0:
            return

        self.state._current_index = index  # temporary, controlled
        text = self.paragraphs[index]
        self.content_box.setText(text)
    
    def toggle_play(self):
        index = self.paragraph_list.currentRow()
        if index < 0:
            return

        if not self.is_playing:
            self.is_playing = True
            self.play_button.setText("⏸ Pause")
            self.status_label.setText("Status: Playing")
            self.status_label.setStyleSheet("color: green;")

            paragraph = self.store.get_para(index)
            explanation_units = self.explainer.explain(paragraph)

            self.player.start(explanation_units, self.state, index)
            self.player.play_next()  # 🔑 ONE sentence only

        else:
            self.is_playing = False
            self.play_button.setText("▶ Play")
            self.status_label.setText("Status: Paused")
            self.status_label.setStyleSheet("color: gray;")

            self.player.pause()
        
    def select_previous(self):
        current = self.paragraph_list.currentRow()
        if current > 0:
            self.paragraph_list.setCurrentRow(current - 1)

    def select_next(self):
        current = self.paragraph_list.currentRow()
        if current < self.paragraph_list.count() - 1:
            self.paragraph_list.setCurrentRow(current + 1)

    def explain_current(self):
        index = self.paragraph_list.currentRow()
        if index >= 0:
            self.status_label.setText(
                f"Status: Ready to explain Paragraph {index + 1}"
            )

    def enter_exam_mode(self):
        self.status_label.setText("Status: Exam Mode")


def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()
