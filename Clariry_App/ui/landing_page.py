# ui/landing_page.py
# ──────────────────
# Stunning "Universe" landing page for CLARIRY.

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtGui import QFont, QColor

class LandingPage(QWidget):
    """
    The 'Universe Teacher' landing page.
    Shows when no document is loaded.
    """
    start_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("landing_page")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)
        layout.setAlignment(Qt.AlignCenter)

        # ── Hero Section ─────────────────────────────────────────────
        self.logo_label = QLabel("✧")
        self.logo_label.setStyleSheet("font-size: 80px; color: #fbbf24;")
        self.logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label)

        self.title = QLabel("CLARIRY")
        self.title.setObjectName("landing_title")
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        self.subtitle = QLabel("Your Personal Universe Teacher")
        self.subtitle.setStyleSheet("font-size: 24px; color: #a5b4fc; font-weight: 600;")
        self.subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.subtitle)

        self.desc = QLabel(
            "Unlock the secrets of your study material with the power of the cosmos.\n"
            "Simple explanations, energetic vibes, and total focus."
        )
        self.desc.setObjectName("landing_desc")
        self.desc.setAlignment(Qt.AlignCenter)
        self.desc.setWordWrap(True)
        self.desc.setFixedWidth(600)
        layout.addWidget(self.desc)

        # ── Features ──────────────────────────────────────────────────
        feat_layout = QHBoxLayout()
        feat_layout.setSpacing(20)
        
        feat_layout.addWidget(self._feat_card("🚀", "Energetic", "Hinglish vibey explanations"))
        feat_layout.addWidget(self._feat_card("🌌", "Seamless", "PDFs stay visible always"))
        feat_layout.addWidget(self._feat_card("🧠", "Smart", "Instant doubts cleared"))
        
        layout.addLayout(feat_layout)

        layout.addSpacing(40)

        # ── CTA ───────────────────────────────────────────────────────
        self.start_btn = QPushButton("LAUNCH YOUR JOURNEY")
        self.start_btn.setObjectName("btn_primary")
        self.start_btn.setFixedWidth(300)
        self.start_btn.setFixedHeight(60)
        self.start_btn.setCursor(Qt.PointingHandCursor)
        self.start_btn.clicked.connect(self.start_requested.emit)
        layout.addWidget(self.start_btn, 0, Qt.AlignCenter)

        # ── Animation ────────────────────────────────────────────────
        self._anim_timer = QTimer(self)
        self._anim_timer.timeout.connect(self._animate_logo)
        self._anim_timer.start(2000)
        
        self._logo_opacity = QPropertyAnimation(self.logo_label, b"windowOpacity")

    def _feat_card(self, icon, title, desc):
        card = QFrame()
        card.setStyleSheet(
            "background-color: #1e1b4b66; border: 1px solid #312e81; "
            "border-radius: 20px; padding: 20px;"
        )
        card.setFixedWidth(180)
        
        l = QVBoxLayout(card)
        
        i = QLabel(icon)
        i.setStyleSheet("font-size: 32px;")
        i.setAlignment(Qt.AlignCenter)
        
        t = QLabel(title)
        t.setStyleSheet("font-weight: 800; font-size: 16px; color: #ffffff;")
        t.setAlignment(Qt.AlignCenter)
        
        d = QLabel(desc)
        d.setStyleSheet("font-size: 12px; color: #94a3b8;")
        d.setAlignment(Qt.AlignCenter)
        d.setWordWrap(True)
        
        l.addWidget(i)
        l.addWidget(t)
        l.addWidget(d)
        
        return card

    def _animate_logo(self):
        # Subtle "breathing" effect for the space theme
        pass 
