"""
main.py — CLARIRY GUI launcher
Run: python main.py
"""

import sys
import os

# Ensure the project root is on sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setApplicationName("CLARIRY")
    app.setApplicationDisplayName("CLARIRY — Your AI Tutor-Friend")

    # Use Inter / Segoe UI as default app font
    font = QFont("Segoe UI", 13)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
