# ui/theme.py
# ─────────────
# CLARIRY dark-mode QSS stylesheet.
# Palette: Deep Navy bg · Midnight panel · Electric Teal accent · White text

DARK_THEME = """
/* ── Universe Teacher Global ───────────────────────────────────────── */
* {
    font-family: 'Outfit', 'Inter', Segoe UI, sans-serif;
    font-size: 13px;
    color: #e2e8f0;
    outline: none;
}

QMainWindow, QWidget#root {
    background-color: #020617; /* Deep Space Black */
}

QWidget {
    background-color: transparent;
}

/* ── Panels ──────────────────────────────────────────────────────── */
QWidget#sidebar {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #0f172a, stop:1 #1e1b4b); /* Nebula Sidebar */
    border-right: 1px solid #312e81;
}

QWidget#center_panel {
    background-color: #020617;
}

QWidget#right_panel {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #0f172a, stop:1 #1e1b4b);
    border-left: 1px solid #312e81;
}

/* ── Header bar ──────────────────────────────────────────────────── */
QWidget#header {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #020617, stop:0.5 #1e1b4b, stop:1 #020617);
    border-bottom: 2px solid #4f46e533;
}

QLabel#app_title {
    font-size: 28px;
    font-weight: 900;
    color: #f1f5f9;
    letter-spacing: 2px;
}

QLabel#app_subtitle {
    font-size: 12px;
    color: #a5b4fc;
    font-weight: 600;
    letter-spacing: 1px;
}

/* ── List widget (Study Guide) ───────────────────────────────────── */
QListWidget {
    background-color: transparent;
    border: none;
    padding: 10px;
}

QListWidget::item {
    padding: 14px 18px;
    border-radius: 12px;
    margin: 6px 0;
    color: #94a3b8;
    background-color: #1e293b55;
    border: 1px solid transparent;
}

QListWidget::item:hover {
    background-color: #312e8155;
    color: #f1f5f9;
    border: 1px solid #4f46e555;
}

QListWidget::item:selected {
    background-color: #4f46e533;
    color: #fbbf24; /* Star Gold */
    border: 1px solid #fbbf2455;
}

/* ── Text areas (Glassmorphism) ──────────────────────────────────── */
QTextEdit, QPlainTextEdit {
    background-color: #0f172a88;
    border: 1px solid #312e81;
    border-radius: 16px;
    padding: 24px;
    color: #f1f5f9;
    line-height: 1.8;
    selection-background-color: #fbbf2433;
    selection-color: #fbbf24;
}

QTextEdit:focus {
    border: 1px solid #6366f1;
}

/* ── Buttons ─────────────────────────────────────────────────────── */
QPushButton {
    background-color: #1e1b4b;
    color: #f1f5f9;
    border: 1px solid #4338ca;
    border-radius: 12px;
    padding: 12px 20px;
    font-size: 13px;
    font-weight: 700;
}

QPushButton:hover {
    background-color: #312e81;
    border-color: #818cf8;
    color: #ffffff;
}

QPushButton:pressed {
    background-color: #1e1b4b;
}

QPushButton#btn_primary {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #4f46e5, stop:1 #7c3aed);
    color: #ffffff;
    border: none;
}

QPushButton#btn_primary:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #6366f1, stop:1 #8b5cf6);
}

QPushButton#btn_exam {
    background-color: transparent;
    border: 2px solid #fbbf24;
    color: #fbbf24;
}

QPushButton#btn_exam:hover {
    background-color: #fbbf2411;
}

QPushButton#btn_exam:checked {
    background-color: #fbbf24;
    color: #020617;
}

/* ── Progress bar ────────────────────────────────────────────────── */
QProgressBar {
    background-color: #1e1b4b;
    border: none;
    border-radius: 6px;
    height: 12px;
    text-align: center;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #7c3aed, stop:0.5 #fbbf24, stop:1 #7c3aed);
    border-radius: 6px;
}

/* ── Labels ──────────────────────────────────────────────────────── */
QLabel#section_title {
    font-size: 12px;
    font-weight: 800;
    color: #6366f1;
    letter-spacing: 3px;
    text-transform: uppercase;
    padding: 16px 12px 8px 12px;
}

QLabel#status_chip {
    font-size: 11px;
    font-weight: 800;
    padding: 6px 16px;
    border-radius: 15px;
    background-color: #1e1b4b;
    color: #a5b4fc;
    border: 1px solid #4338ca;
}

/* ── Toast Notifications ─────────────────────────────────────────── */
QWidget#toast_notif {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #1e1b4b, stop:1 #312e81);
    border: 2px solid #fbbf2433;
    border-radius: 14px;
}

QLabel#toast_msg {
    color: #f1f5f9;
    font-weight: 700;
    font-size: 13px;
}

/* ── Landing Page Specific ──────────────────────────────────────── */
QLabel#landing_title {
    font-size: 64px;
    font-weight: 900;
    color: #ffffff;
}

QLabel#landing_desc {
    font-size: 18px;
    color: #94a3b8;
    line-height: 1.6;
}

/* ── Scroll bars ─────────────────────────────────────────────────── */
QScrollBar:vertical {
    background: transparent;
    width: 8px;
    margin: 4px;
}

QScrollBar::handle:vertical {
    background: #312e81;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #4f46e5;
}
"""

# Status chip colours (used programmatically)
STATUS_COLORS = {
    "idle":     ("background-color: #1e1b4b; color: #a5b4fc; border: 1px solid #4338ca;", "✧ Space Idle"),
    "thinking": ("background-color: #4c1d95; color: #f5f3ff; border: 1px solid #8b5cf6;", "⟳ Processing Universe…"),
    "speaking": ("background-color: #1e3a8a; color: #dbeafe; border: 1px solid #3b82f6;", "▶ Radiating Wisdom"),
    "paused":   ("background-color: #713f12; color: #fef3c7; border: 1px solid #fbbf24;", "⏸ Orbiting"),
    "error":    ("background-color: #7f1d1d; color: #fca5a5; border: 1px solid #ef4444;", "✗ Black Hole Error"),
}

