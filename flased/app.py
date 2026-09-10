import sys
import os
import re
from typing import Optional

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QStackedWidget, QFrame, QDialog,
    QSplashScreen, QLineEdit, QTextEdit, QMessageBox, QInputDialog,
    QScrollArea, QComboBox, QProgressBar, QSizePolicy
)
from PySide6.QtCore import Qt, QTimer, QSize, QThread, Signal
from PySide6.QtGui import QColor, QPainter, QFont, QPixmap, QKeySequence, QShortcut, QPalette

from engine import generate_flashcards_for_module
import database
from session import ReviewSession
import icons

MATTE_THEME = """
/* Global Window & Surfaces */
QMainWindow, QWidget#CentralWidget, QStackedWidget, 
QWidget#PageModules, QWidget#PageAdd, QWidget#PageReview, 
QWidget#PageDeck, QWidget#DeckContainer,
QScrollArea, QWidget#ScrollContainer {
    background-color: #070709;
    color: #ededed;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
    font-size: 13px;
}

/* Sidebar */
QFrame#Sidebar {
    background-color: #0a0a0d;
    border-right: 1px solid #141418;
}

QPushButton#NavBtn {
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: 6px;
    padding: 9px 12px;
    text-align: left;
    font-size: 13px;
    font-weight: 500;
    color: #82828c;
    outline: none;
}
QPushButton#NavBtn:hover {
    background-color: #121216;
    color: #ededed;
}
QPushButton#NavBtn[active="true"] {
    background-color: #15151c;
    color: #ffffff;
    font-weight: 600;
    border: 1px solid #20202a;
}

/* ScrollArea & Scrollbars */
QScrollArea {
    border: none;
    background-color: #070709;
}
QScrollBar:vertical {
    background: transparent;
    width: 6px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #1a1a22;
    min-height: 28px;
    border-radius: 3px;
}
QScrollBar::handle:vertical:hover {
    background: #2a2a36;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Subject & Module Cards */
QFrame#SubjectCard {
    background-color: #0e0e12;
    border: 1px solid #181820;
    border-radius: 10px;
}
QFrame#ModuleRow {
    background-color: #121217;
    border: 1px solid #181820;
    border-radius: 6px;
}
QFrame#ModuleRow:hover {
    background-color: #16161d;
    border-color: #22222d;
}

/* General Buttons */
QPushButton {
    background-color: #131318;
    border: 1px solid #1d1d26;
    border-radius: 6px;
    padding: 7px 13px;
    font-weight: 500;
    color: #d4d4d8;
    outline: none;
}
QPushButton:hover {
    background-color: #1a1a22;
    border-color: #272734;
    color: #ffffff;
}
QPushButton:pressed {
    background-color: #101014;
}
QPushButton:disabled {
    background-color: #0e0e12;
    border-color: #15151b;
    color: #404048;
}

/* High-Contrast White Action Button */
QPushButton#PrimaryBtn {
    background-color: #ffffff;
    border: 1px solid #ffffff;
    color: #09090b;
    font-weight: 600;
}
QPushButton#PrimaryBtn:hover {
    background-color: #e4e4e7;
    border-color: #e4e4e7;
}

/* Learn All Button */
QPushButton#LearnAllBtn {
    background-color: #13131b;
    border: 1px solid #20202d;
    border-radius: 6px;
    padding: 9px 14px;
    font-size: 12.5px;
    font-weight: 600;
    color: #ededed;
}
QPushButton#LearnAllBtn:hover {
    background-color: #191924;
    border-color: #2e2e3f;
    color: #ffffff;
}

/* Action Icon Buttons */
QPushButton#IconBtn {
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: 5px;
    padding: 5px 8px;
    color: #787882;
    font-size: 12px;
}
QPushButton#IconBtn:hover {
    background-color: #16161c;
    color: #f4f4f5;
    border-color: #1f1f28;
}
QPushButton#IconBtnDanger:hover {
    background-color: #201014;
    color: #f87171;
    border-color: #38151b;
}

/* Quota Cards */
QFrame#SidebarQuotaCard {
    background-color: #0c0c10;
    border: 1px solid #16161f;
    border-radius: 8px;
}
QFrame#AddQuotaCard {
    background-color: #0d0d12;
    border: 1px solid #181822;
    border-radius: 8px;
}

/* Inputs */
QLineEdit, QTextEdit, QComboBox {
    background-color: #0f0f13;
    border: 1px solid #1a1a22;
    border-radius: 6px;
    padding: 9px 12px;
    color: #ededed;
    font-size: 13px;
    selection-background-color: #20202c;
}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border-color: #3b82f6;
    background-color: #121217;
}
QComboBox QAbstractItemView {
    background-color: #0f0f13;
    border: 1px solid #1a1a22;
    color: #ededed;
    selection-background-color: #181822;
    outline: none;
}

/* Review Screen */
QFrame#ReviewCard {
    background-color: #0e0e12;
    border: 1px solid #181820;
    border-radius: 12px;
}
QProgressBar {
    background-color: #111115;
    border: none;
    height: 3px;
    text-align: center;
    color: transparent;
}
QProgressBar::chunk {
    background-color: #10b981;
}

/* Reveal & Rating Controls */
QPushButton#RevealActionBtn {
    background-color: #14141c;
    border: 1px solid #232330;
    border-radius: 7px;
    padding: 12px 28px;
    font-size: 13.5px;
    font-weight: 600;
    color: #ffffff;
}
QPushButton#RevealActionBtn:hover {
    background-color: #1c1c27;
    border-color: #333344;
}

QPushButton#RateDidntKnow {
    background-color: #14090b;
    border: 1px solid #361017;
    border-radius: 7px;
    padding: 11px 16px;
    color: #f87171;
    font-size: 13px;
    font-weight: 600;
}
QPushButton#RateDidntKnow:hover {
    background-color: #200c11;
    border-color: #e11d48;
    color: #ffffff;
}

QPushButton#RateABit {
    background-color: #140d05;
    border: 1px solid #381e05;
    border-radius: 7px;
    padding: 11px 16px;
    color: #fbbf24;
    font-size: 13px;
    font-weight: 600;
}
QPushButton#RateABit:hover {
    background-color: #221408;
    border-color: #f59e0b;
    color: #ffffff;
}

QPushButton#RateIKnow {
    background-color: #07120c;
    border: 1px solid #09301b;
    border-radius: 7px;
    padding: 11px 16px;
    color: #4ade80;
    font-size: 13px;
    font-weight: 600;
}
QPushButton#RateIKnow:hover {
    background-color: #0b1c13;
    border-color: #10b981;
    color: #ffffff;
}

/* Deck Browser & Card Manager */
QFrame#DeckCardItem {
    background-color: #0d0d12;
    border: 1px solid #181824;
    border-radius: 10px;
}
QFrame#DeckCardItem:hover {
    background-color: #101017;
    border-color: #242436;
}

/* Modal Dialog Box */
QFrame#ModalBox {
    background-color: #0d0d14;
    border: 1px solid #232336;
    border-radius: 14px;
}
QDialog {
    background-color: #09090d;
    color: #ededed;
}

/* Search Bar */
QLineEdit#SearchInput {
    background-color: #0e0e14;
    border: 1px solid #1c1c28;
    border-radius: 7px;
    padding: 8px 14px;
    color: #ededed;
    font-size: 13px;
}
QLineEdit#SearchInput:focus {
    border-color: #6366f1;
    background-color: #12121c;
}
"""

class SplashScreen(QSplashScreen):
    def __init__(self):
        pixmap = QPixmap(360, 220)
        pixmap.fill(QColor("#070709"))
        super().__init__(pixmap)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Outer subtle frame
        painter.setPen(QColor("#181822"))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(1, 1, 358, 218, 12, 12)
        
        # Minimalist 'F' Logo badge
        painter.setBrush(QColor("#12121a"))
        painter.setPen(QColor("#242436"))
        painter.drawRoundedRect(158, 42, 44, 44, 10, 10)
        
        painter.setPen(QColor("#ffffff"))
        painter.setFont(QFont("Segoe UI", 20, QFont.Bold))
        painter.drawText(158, 42, 44, 44, Qt.AlignCenter, "F")
        
        # Title "FLASED"
        painter.setPen(QColor("#ffffff"))
        painter.setFont(QFont("Segoe UI", 15, QFont.Bold))
        painter.drawText(0, 104, 360, 24, Qt.AlignCenter, "FLASED")
        
        # Creator "sceed"
        painter.setPen(QColor("#52525e"))
        painter.setFont(QFont("Segoe UI", 10, QFont.Medium))
        painter.drawText(0, 136, 360, 20, Qt.AlignCenter, "sceed")
        
        painter.end()
        self.setPixmap(pixmap)


def format_explanation_html(text: str) -> str:
    """Parse stored bullet explanation text into rich, premium HTML.
    
    Stored format per bullet line:
        • **E** — **E-Commerce Scope**: Focuses on commercial transactions...
    Or plain summary intro line (no bullet).
    """
    if not text:
        return ""
    
    lines = [l.strip() for l in text.strip().split("\n") if l.strip()]
    html_parts = []
    
    # Pattern for structured bullet: • **X** — **Keyword**: description
    # Or simpler: • **X** — Keyword: description
    bullet_structured = re.compile(
        r'^[•\-\*]\s*'
        r'\*\*([A-Z0-9])\*\*'          # letter in ** **
        r'\s*[—\-–]\s*'
        r'\*\*([^\*]+)\*\*'            # keyword in ** **
        r'[:\s]+(.+)$'                  # colon then description
    )
    # Simpler bullet: • **X** — Keyword: description  (keyword not bolded)
    bullet_simple = re.compile(
        r'^[•\-\*]\s*'
        r'\*\*([A-Z0-9])\*\*'          # letter
        r'\s*[—\-–]\s*'
        r'([^:]+)'
        r'[:\s]+(.+)$'
    )
    # Plain bullet: • some text  OR - some text
    bullet_plain = re.compile(r'^[•\-\*]\s+(.+)$')
    
    for line in lines:
        m = bullet_structured.match(line)
        if not m:
            m = bullet_simple.match(line)
        
        if m:
            letter = m.group(1).strip().upper()
            keyword = m.group(2).strip()
            desc = m.group(3).strip()
            # Escape any remaining ** markers in desc
            desc = re.sub(r'\*\*(.*?)\*\*', r'<b style="color:#e2e8f0">\1</b>', desc)
            # Use table layout (Qt HTML4 compatible, no flexbox)
            html_parts.append(
                f'<table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:11px;">'
                f'<tr>'
                f'<td width="40" valign="top" style="padding-right:12px; padding-top:1px;">'
                f'<span style="'
                f'background-color:#0f2437; border:1px solid #1e4976; border-radius:6px; '
                f'color:#38bdf8; font-size:13px; font-weight:800; '
                f'padding:3px 7px; white-space:nowrap;">'
                f'{letter}</span>'
                f'</td>'
                f'<td valign="top" style="line-height:1.65;">'
                f'<span style="color:#f1f5f9; font-weight:700; font-size:13.5px;">{keyword}</span>'
                f'<span style="color:#52525b; font-size:12.5px;"> &mdash; </span>'
                f'<span style="color:#cbd5e1; font-size:13px;">{desc}</span>'
                f'</td>'
                f'</tr>'
                f'</table>'
            )
        else:
            m_plain = bullet_plain.match(line)
            if m_plain:
                content = m_plain.group(1).strip()
                content = re.sub(r'\*\*(.*?)\*\*', r'<b style="color:#e2e8f0">\1</b>', content)
                html_parts.append(
                    f'<table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:10px;">'
                    f'<tr>'
                    f'<td width="16" valign="top" style="color:#38bdf8; font-weight:700; padding-right:8px; padding-top:1px;">&rsaquo;</td>'
                    f'<td style="color:#cbd5e1; font-size:13px; line-height:1.6;">{content}</td>'
                    f'</tr>'
                    f'</table>'
                )
            else:
                # Summary / intro line (no bullet) — shown as muted italic header
                clean = re.sub(r'\*\*(.*?)\*\*', r'<b style="color:#e2e8f0">\1</b>', line)
                html_parts.append(
                    f'<p style="color:#71717a; font-size:12.5px; font-style:italic; '
                    f'margin:0 0 12px 0; line-height:1.6; '
                    f'border-bottom:1px solid #1a1a2e; padding-bottom:8px;">'
                    f'{clean}</p>'
                )
    
    return "".join(html_parts)


class GenerationWorker(QThread):
    finished = Signal(object)
    error = Signal(str)

    def __init__(self, module_title: str, content: str):
        super().__init__()
        self.module_title = module_title
        self.content = content

    def run(self):
        try:
            res = generate_flashcards_for_module(self.module_title, self.content)
            self.finished.emit(res)
        except Exception as e:
            self.error.emit(str(e))


class GenerationLoadingModal(QDialog):
    """
    Minimalist modal overlay box that displays while AI is generating flashcards.
    Displays 'Analyzing' then transitions to 'Ready'.
    """
    def __init__(self, parent=None, module_title=""):
        super().__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setModal(True)
        self.module_title = module_title
        self.created_module_id = None
        self.on_view_cards = None
        
        self.resize(340, 190)
        if parent:
            p_geom = parent.geometry()
            self.move(
                p_geom.x() + (p_geom.width() - 340) // 2,
                p_geom.y() + (p_geom.height() - 190) // 2
            )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.box = QFrame()
        self.box.setObjectName("ModalBox")
        self.box.setStyleSheet("""
            QFrame#ModalBox {
                background-color: #0c0c12;
                border: 1px solid #202030;
                border-radius: 12px;
            }
        """)
        box_layout = QVBoxLayout(self.box)
        box_layout.setContentsMargins(28, 26, 28, 26)
        box_layout.setSpacing(12)
        box_layout.setAlignment(Qt.AlignCenter)

        # Status Icon Container
        self.icon_badge = QLabel()
        self.icon_badge.setFixedSize(48, 48)
        self.icon_badge.setAlignment(Qt.AlignCenter)
        self.icon_badge.setStyleSheet(
            "background-color: #12121e; border: 1px solid #1f1f34; border-radius: 24px;"
        )
        self.icon_badge.setPixmap(icons.get_pixmap("sparkles", "#818cf8", 20))

        # Title — single word: Analyzing
        self.lbl_title = QLabel("Analyzing")
        self.lbl_title.setStyleSheet("font-size: 16px; font-weight: 700; color: #ffffff;")
        self.lbl_title.setAlignment(Qt.AlignCenter)

        self.lbl_subtitle = QLabel("")
        self.lbl_subtitle.setStyleSheet("font-size: 12px; color: #71717a;")
        self.lbl_subtitle.setAlignment(Qt.AlignCenter)
        self.lbl_subtitle.hide()

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setFixedHeight(3)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #151520;
                border: none;
                border-radius: 1px;
            }
            QProgressBar::chunk {
                background-color: #6366f1;
                border-radius: 1px;
            }
        """)

        # Button Row
        self.btn_row = QHBoxLayout()
        self.btn_row.setSpacing(10)
        self.btn_row.setAlignment(Qt.AlignCenter)

        self.btn_view_cards = QPushButton("View")
        self.btn_view_cards.setObjectName("PrimaryBtn")
        self.btn_view_cards.setFixedHeight(34)
        self.btn_view_cards.setFocusPolicy(Qt.NoFocus)
        self.btn_view_cards.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                border: 1px solid #ffffff;
                color: #09090b;
                font-weight: 600;
                border-radius: 6px;
                padding: 6px 18px;
                font-size: 12.5px;
            }
            QPushButton:hover {
                background-color: #e4e4e7;
            }
        """)
        self.btn_view_cards.clicked.connect(self._on_view_clicked)

        self.btn_done = QPushButton("Done")
        self.btn_done.setFixedHeight(34)
        self.btn_done.setFocusPolicy(Qt.NoFocus)
        self.btn_done.setStyleSheet("""
            QPushButton {
                background-color: #161622;
                border: 1px solid #26263a;
                color: #d4d4d8;
                font-weight: 500;
                border-radius: 6px;
                padding: 6px 18px;
                font-size: 12.5px;
            }
            QPushButton:hover {
                background-color: #1f1f30;
                color: #ffffff;
            }
        """)
        self.btn_done.clicked.connect(self.accept)

        self.btn_row.addWidget(self.btn_view_cards)
        self.btn_row.addWidget(self.btn_done)

        self.btn_container = QWidget()
        self.btn_container.setLayout(self.btn_row)
        self.btn_container.hide()

        box_layout.addWidget(self.icon_badge, 0, Qt.AlignCenter)
        box_layout.addWidget(self.lbl_title)
        box_layout.addWidget(self.lbl_subtitle)
        box_layout.addSpacing(2)
        box_layout.addWidget(self.progress_bar)
        box_layout.addWidget(self.btn_container)

        layout.addWidget(self.box)

    def set_success(self, card_count: int, module_id: int):
        self.created_module_id = module_id
        self.icon_badge.setStyleSheet(
            "background-color: #064e3b; border: 1px solid #059669; border-radius: 24px;"
        )
        self.icon_badge.setPixmap(icons.get_pixmap("check-circle", "#34d399", 22))
        self.lbl_title.setText("Ready")
        self.lbl_subtitle.setText(f"{card_count} cards")
        self.lbl_subtitle.show()
        self.progress_bar.hide()
        self.btn_container.show()

    def set_error(self, err_msg: str):
        self.icon_badge.setStyleSheet(
            "background-color: #3b1118; border: 1px solid #e11d48; border-radius: 24px;"
        )
        self.icon_badge.setPixmap(icons.get_pixmap("x", "#f87171", 20))
        self.lbl_title.setText("Error")
        self.lbl_subtitle.setText(err_msg)
        self.lbl_subtitle.show()
        self.progress_bar.hide()
        self.btn_view_cards.hide()
        self.btn_done.setText("Close")
        self.btn_container.show()

    def _on_view_clicked(self):
        self.accept()
        if self.on_view_cards and self.created_module_id is not None:
            self.on_view_cards(self.created_module_id)


class FlashcardEditDialog(QDialog):
    """
    Modal dialog to create or edit an individual flashcard.
    """
    def __init__(self, parent=None, card_data=None, is_new=False):
        super().__init__(parent)
        self.setWindowTitle("New" if is_new else "Edit")
        self.resize(520, 480)
        self.is_new = is_new
        self.card_data = card_data or {}
        self.setStyleSheet(MATTE_THEME)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)
        
        title_lbl = QLabel("New" if is_new else "Edit")
        title_lbl.setStyleSheet("font-size: 16px; font-weight: 700; color: #ffffff;")
        layout.addWidget(title_lbl)
        
        # Concept Group
        lbl_concept = QLabel("Topic")
        lbl_concept.setStyleSheet("font-weight: 600; color: #a1a1aa; font-size: 12px;")
        self.input_concept = QLineEdit()
        self.input_concept.setPlaceholderText("Topic")
        self.input_concept.setText(self.card_data.get("concept_group", ""))
        layout.addWidget(lbl_concept)
        layout.addWidget(self.input_concept)
        
        # Question
        lbl_q = QLabel("Question")
        lbl_q.setStyleSheet("font-weight: 600; color: #a1a1aa; font-size: 12px;")
        self.input_q = QTextEdit()
        self.input_q.setPlaceholderText("Question")
        self.input_q.setFixedHeight(60)
        self.input_q.setPlainText(self.card_data.get("question", ""))
        layout.addWidget(lbl_q)
        layout.addWidget(self.input_q)
        
        # Explanation
        lbl_exp = QLabel("Answer")
        lbl_exp.setStyleSheet("font-weight: 600; color: #a1a1aa; font-size: 12px;")
        self.input_exp = QTextEdit()
        self.input_exp.setPlaceholderText("Answer bullets")
        self.input_exp.setPlainText(self.card_data.get("explanation", ""))
        layout.addWidget(lbl_exp)
        layout.addWidget(self.input_exp)
        
        # Memory Code
        lbl_mem = QLabel("Code")
        lbl_mem.setStyleSheet("font-weight: 600; color: #a1a1aa; font-size: 12px;")
        self.input_mem = QLineEdit()
        self.input_mem.setPlaceholderText("Acronym")
        self.input_mem.setText(self.card_data.get("memory_code", "") or "")
        layout.addWidget(lbl_mem)
        layout.addWidget(self.input_mem)
        
        # Button Row
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self.reject)
        
        self.btn_save = QPushButton("Save")
        self.btn_save.setObjectName("PrimaryBtn")
        self.btn_save.clicked.connect(self.save_data)
        
        btn_row.addWidget(self.btn_cancel)
        btn_row.addWidget(self.btn_save)
        layout.addLayout(btn_row)
        
    def save_data(self):
        q = self.input_q.toPlainText().strip()
        exp = self.input_exp.toPlainText().strip()
        if not q or not exp:
            QMessageBox.warning(self, "Incomplete", "Question and Answer required.")
            return
        self.accept()
        
    def get_data(self):
        return {
            "concept_group": self.input_concept.text().strip().upper() or "GENERAL",
            "question": self.input_q.toPlainText().strip(),
            "explanation": self.input_exp.toPlainText().strip(),
            "memory_code": self.input_mem.text().strip().upper() or None
        }


class ApiKeyDialog(QDialog):
    """
    Minimalist dialog for setting / replacing the Gemini API key.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("API Key")
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setModal(True)
        self.resize(360, 210)
        if parent:
            p = parent.geometry()
            self.move(p.x() + (p.width() - 360) // 2,
                      p.y() + (p.height() - 210) // 2)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        box = QFrame()
        box.setObjectName("ModalBox")
        box.setStyleSheet("""
            QFrame#ModalBox {
                background-color: #0c0c12;
                border: 1px solid #202030;
                border-radius: 12px;
            }
        """)
        layout = QVBoxLayout(box)
        layout.setContentsMargins(26, 22, 26, 22)
        layout.setSpacing(12)

        # Title row
        title_row = QHBoxLayout()
        title_row.setSpacing(8)
        icon_lbl = QLabel()
        icon_lbl.setPixmap(icons.get_pixmap("zap", "#818cf8", 14))
        lbl_title = QLabel("API Key")
        lbl_title.setStyleSheet("font-size: 14px; font-weight: 700; color: #ffffff;")
        title_row.addWidget(icon_lbl)
        title_row.addWidget(lbl_title)
        title_row.addStretch()
        layout.addLayout(title_row)

        # Current key status
        existing = database.get_api_key()
        status_text = f"···{existing[-6:]}" if len(existing) > 6 else ("Set" if existing else "None")
        self.lbl_status = QLabel(status_text)
        self.lbl_status.setStyleSheet("font-size: 11px; color: #52525e; font-family: monospace;")
        layout.addWidget(self.lbl_status)

        # Input
        self.input_key = QLineEdit()
        self.input_key.setPlaceholderText("Paste API key")
        self.input_key.setEchoMode(QLineEdit.Password)
        self.input_key.setMinimumHeight(36)
        self.input_key.setStyleSheet("""
            QLineEdit {
                background-color: #0f0f16;
                border: 1px solid #252538;
                border-radius: 6px;
                padding: 7px 12px;
                color: #ededed;
                font-size: 13px;
                font-family: monospace;
            }
            QLineEdit:focus { border-color: #6366f1; }
        """)
        layout.addWidget(self.input_key)

        # Toggle visibility checkbox
        self.chk_show = QPushButton("Show")
        self.chk_show.setCheckable(True)
        self.chk_show.setObjectName("IconBtn")
        self.chk_show.setFocusPolicy(Qt.NoFocus)
        self.chk_show.setFixedHeight(28)
        self.chk_show.toggled.connect(
            lambda checked: self.input_key.setEchoMode(
                QLineEdit.Normal if checked else QLineEdit.Password
            )
        )

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        btn_row.addWidget(self.chk_show)
        btn_row.addStretch()

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setFocusPolicy(Qt.NoFocus)
        btn_cancel.setFixedHeight(32)
        btn_cancel.clicked.connect(self.reject)

        self.btn_save = QPushButton("Save")
        self.btn_save.setObjectName("PrimaryBtn")
        self.btn_save.setFocusPolicy(Qt.NoFocus)
        self.btn_save.setFixedHeight(32)
        self.btn_save.clicked.connect(self._save)

        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(self.btn_save)
        layout.addLayout(btn_row)

        outer.addWidget(box)

    def _save(self):
        key = self.input_key.text().strip()
        if key:
            database.set_api_key(key)
        self.accept()


class FlasedApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FLASED")
        self.setWindowIcon(icons.get_icon("logo", size=32))
        self.resize(1160, 750)
        self.setMinimumSize(940, 600)
        
        # Force dark titlebar on Windows
        try:
            from ctypes import windll, byref, c_int, sizeof
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            hwnd = int(self.winId())
            windll.dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE,
                byref(c_int(1)), sizeof(c_int)
            )
        except Exception:
            pass
        
        # Apply dark palette globally
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#070709"))
        palette.setColor(QPalette.WindowText, QColor("#ededed"))
        palette.setColor(QPalette.Base, QColor("#070709"))
        palette.setColor(QPalette.AlternateBase, QColor("#0e0e12"))
        palette.setColor(QPalette.Text, QColor("#ededed"))
        palette.setColor(QPalette.Button, QColor("#131318"))
        palette.setColor(QPalette.ButtonText, QColor("#ededed"))
        self.setPalette(palette)
        
        self.setStyleSheet(MATTE_THEME)
        
        self.current_session: Optional[ReviewSession] = None
        self.is_card_revealed = False
        self.current_deck_module_id: Optional[int] = None
        self.current_deck_cards = []
        self.deck_card_widgets = []
        self._current_gen_worker = None

        database.init_db()
        self.init_ui()
        self.init_shortcuts()
        self.load_subjects_overview()
        self.update_quota_display()

    def init_ui(self):
        root = QWidget()
        root.setObjectName("CentralWidget")
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        
        # Sidebar
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(210)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(14, 20, 14, 20)
        sidebar_layout.setSpacing(6)
        
        # Brand (Minimalist 'F' Logo & Title)
        brand_row = QHBoxLayout()
        brand_row.setSpacing(10)
        brand_row.setContentsMargins(2, 2, 2, 18)
        
        logo_lbl = QLabel()
        logo_lbl.setPixmap(icons.get_pixmap("logo", size=24))
        
        lbl_title = QLabel("FLASED")
        lbl_title.setStyleSheet("font-size: 15px; font-weight: 800; color: #ffffff; letter-spacing: 1px;")
        
        brand_row.addWidget(logo_lbl)
        brand_row.addWidget(lbl_title)
        brand_row.addStretch()
        sidebar_layout.addLayout(brand_row)
        
        # Nav Buttons — one word each
        self.btn_nav_modules = QPushButton("Modules")
        self.btn_nav_modules.setObjectName("NavBtn")
        self.btn_nav_modules.setIcon(icons.get_icon("folder", "#82828c", 15))
        self.btn_nav_modules.setIconSize(QSize(15, 15))
        self.btn_nav_modules.setProperty("active", "true")
        self.btn_nav_modules.setFocusPolicy(Qt.NoFocus)
        self.btn_nav_modules.clicked.connect(lambda: self.switch_page(0))
        
        self.btn_nav_add = QPushButton("Add")
        self.btn_nav_add.setObjectName("NavBtn")
        self.btn_nav_add.setIcon(icons.get_icon("sparkles", "#82828c", 15))
        self.btn_nav_add.setIconSize(QSize(15, 15))
        self.btn_nav_add.setFocusPolicy(Qt.NoFocus)
        self.btn_nav_add.clicked.connect(lambda: self.switch_page(1))
        
        self.btn_nav_review = QPushButton("Review")
        self.btn_nav_review.setObjectName("NavBtn")
        self.btn_nav_review.setIcon(icons.get_icon("cards", "#82828c", 15))
        self.btn_nav_review.setIconSize(QSize(15, 15))
        self.btn_nav_review.setFocusPolicy(Qt.NoFocus)
        self.btn_nav_review.clicked.connect(lambda: self.switch_page(2))
        
        sidebar_layout.addWidget(self.btn_nav_modules)
        sidebar_layout.addWidget(self.btn_nav_add)
        sidebar_layout.addWidget(self.btn_nav_review)
        sidebar_layout.addStretch()
        
        # Quota Card in Sidebar
        self.sidebar_quota_card = QFrame()
        self.sidebar_quota_card.setObjectName("SidebarQuotaCard")
        sidebar_quota_layout = QVBoxLayout(self.sidebar_quota_card)
        sidebar_quota_layout.setContentsMargins(11, 10, 11, 10)
        sidebar_quota_layout.setSpacing(6)
        
        sq_header = QHBoxLayout()
        sq_icon = QLabel()
        sq_icon.setPixmap(icons.get_pixmap("activity", "#82828c", 13))
        sq_title = QLabel("Quota")
        sq_title.setStyleSheet("font-size: 11px; font-weight: 600; color: #82828c; letter-spacing: 0.3px;")
        
        self.lbl_sidebar_quota_val = QLabel("0 / 50")
        self.lbl_sidebar_quota_val.setStyleSheet("font-size: 11px; font-weight: 600; color: #d4d4d8;")
        
        sq_header.addWidget(sq_icon)
        sq_header.addSpacing(2)
        sq_header.addWidget(sq_title)
        sq_header.addStretch()
        sq_header.addWidget(self.lbl_sidebar_quota_val)
        
        self.sidebar_quota_bar = QProgressBar()
        self.sidebar_quota_bar.setRange(0, 100)
        self.sidebar_quota_bar.setFixedHeight(3)
        self.sidebar_quota_bar.setTextVisible(False)
        
        self.lbl_sidebar_quota_status = QLabel("50 left")
        self.lbl_sidebar_quota_status.setStyleSheet("font-size: 10px; color: #63636e;")
        
        sidebar_quota_layout.addLayout(sq_header)
        sidebar_quota_layout.addWidget(self.sidebar_quota_bar)
        sidebar_quota_layout.addWidget(self.lbl_sidebar_quota_status)
        
        self.sidebar_quota_card.mousePressEvent = lambda e: self.prompt_edit_quota_limit()
        self.sidebar_quota_card.setCursor(Qt.PointingHandCursor)
        self.sidebar_quota_card.setToolTip("Quota")
        
        sidebar_layout.addWidget(self.sidebar_quota_card)

        # API Key button — sits just below the quota card
        self.btn_api_key = QPushButton("Key")
        self.btn_api_key.setObjectName("NavBtn")
        self.btn_api_key.setIcon(icons.get_icon("zap", "#82828c", 14))
        self.btn_api_key.setIconSize(QSize(14, 14))
        self.btn_api_key.setFocusPolicy(Qt.NoFocus)
        self.btn_api_key.setToolTip("Set API Key")
        self.btn_api_key.clicked.connect(self.prompt_set_api_key)
        sidebar_layout.addWidget(self.btn_api_key)
        
        # Stacked Pages
        self.stack = QStackedWidget()
        
        self.page_modules = QWidget()
        self.page_modules.setObjectName("PageModules")
        self.init_modules_page()
        
        self.page_add = QWidget()
        self.page_add.setObjectName("PageAdd")
        self.init_add_page()
        
        self.page_review = QWidget()
        self.page_review.setObjectName("PageReview")
        self.init_review_page()

        self.page_deck = QWidget()
        self.page_deck.setObjectName("PageDeck")
        self.init_deck_page()
        
        self.stack.addWidget(self.page_modules) # 0
        self.stack.addWidget(self.page_add)     # 1
        self.stack.addWidget(self.page_review)  # 2
        self.stack.addWidget(self.page_deck)    # 3
        
        root_layout.addWidget(sidebar)
        root_layout.addWidget(self.stack)
        
        self.setCentralWidget(root)

    def init_shortcuts(self):
        """Global key shortcuts that will NOT be blocked by button focus."""
        self.sc_space = QShortcut(QKeySequence(Qt.Key_Space), self)
        self.sc_space.activated.connect(self.on_space_pressed)
        
        self.sc_1 = QShortcut(QKeySequence(Qt.Key_1), self)
        self.sc_1.activated.connect(lambda: self.on_number_rating("Didn't know"))
        
        self.sc_2 = QShortcut(QKeySequence(Qt.Key_2), self)
        self.sc_2.activated.connect(lambda: self.on_number_rating("A bit"))
        
        self.sc_3 = QShortcut(QKeySequence(Qt.Key_3), self)
        self.sc_3.activated.connect(lambda: self.on_number_rating("I know"))
        
        self.sc_esc = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.sc_esc.activated.connect(lambda: self.switch_page(0))

    def switch_page(self, index: int):
        self.stack.setCurrentIndex(index)
        
        self.btn_nav_modules.setProperty("active", "true" if index in (0, 3) else "false")
        self.btn_nav_add.setProperty("active", "true" if index == 1 else "false")
        self.btn_nav_review.setProperty("active", "true" if index == 2 else "false")
        
        for btn in [self.btn_nav_modules, self.btn_nav_add, self.btn_nav_review]:
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            
        if index == 0:
            self.load_subjects_overview()
            self.update_quota_display()
        elif index == 1:
            self.refresh_add_page_subjects()
            self.update_quota_display()
            self.update_quota_display()

    # =========================================================================
    # Page 0: Subjects & Modules Overview
    # =========================================================================
    def init_modules_page(self):
        layout = QVBoxLayout(self.page_modules)
        layout.setContentsMargins(40, 32, 40, 32)
        layout.setSpacing(22)
        
        # Header Row
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Modules")
        lbl_header.setStyleSheet("font-size: 20px; font-weight: 700; color: #ffffff; letter-spacing: -0.4px;")
        
        self.btn_new_subject = QPushButton("+ New")
        self.btn_new_subject.setObjectName("PrimaryBtn")
        self.btn_new_subject.setFocusPolicy(Qt.NoFocus)
        self.btn_new_subject.clicked.connect(self.prompt_create_subject)
        
        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_new_subject)
        
        # Scroll Area for Subject Folders
        self.subjects_scroll = QScrollArea()
        self.subjects_scroll.setWidgetResizable(True)
        self.subjects_container = QWidget()
        self.subjects_container.setObjectName("ScrollContainer")
        self.subjects_layout = QVBoxLayout(self.subjects_container)
        self.subjects_layout.setContentsMargins(0, 4, 10, 20)
        self.subjects_layout.setSpacing(16)
        self.subjects_layout.addStretch()
        
        self.subjects_scroll.setWidget(self.subjects_container)
        
        layout.addLayout(header_layout)
        layout.addWidget(self.subjects_scroll)

    def load_subjects_overview(self):
        while self.subjects_layout.count() > 1:
            child = self.subjects_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        subjects = database.get_subjects_and_modules()
        
        if not subjects:
            empty_lbl = QLabel("Empty")
            empty_lbl.setStyleSheet("color: #52525b; font-size: 14px; padding: 48px 0;")
            empty_lbl.setAlignment(Qt.AlignCenter)
            self.subjects_layout.insertWidget(0, empty_lbl)
            return

        for idx, sub in enumerate(subjects):
            card = self.create_subject_card(sub)
            self.subjects_layout.insertWidget(idx, card)

    def create_subject_card(self, sub: dict) -> QFrame:
        card = QFrame()
        card.setObjectName("SubjectCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(12)
        
        subject_id = sub["id"]
        subject_title = sub["title"]
        modules = sub["modules"]
        total_cards = sub["total_cards"]
        
        # Header Row
        header_row = QHBoxLayout()
        header_row.setSpacing(10)
        
        folder_icon = QLabel()
        folder_icon.setPixmap(icons.get_pixmap("folder", "#82828c", 16))
        
        title_label = QLabel(subject_title)
        title_label.setStyleSheet("font-size: 15px; font-weight: 600; color: #ffffff;")
        
        badge = QLabel(str(total_cards))
        badge.setStyleSheet("background-color: #121217; border: 1px solid #1c1c24; border-radius: 4px; padding: 2px 7px; font-size: 11px; font-weight: 500; color: #71717a;")
        
        btn_rename = QPushButton("Rename")
        btn_rename.setObjectName("IconBtn")
        btn_rename.setIcon(icons.get_icon("edit", "#787882", 13))
        btn_rename.setFocusPolicy(Qt.NoFocus)
        btn_rename.clicked.connect(lambda checked, s_id=subject_id, s_title=subject_title: self.prompt_rename_subject(s_id, s_title))
        
        btn_delete = QPushButton("Delete")
        btn_delete.setObjectName("IconBtn")
        btn_delete.setIcon(icons.get_icon("trash", "#787882", 13))
        btn_delete.setFocusPolicy(Qt.NoFocus)
        btn_delete.clicked.connect(lambda checked, s_id=subject_id, s_title=subject_title: self.confirm_delete_subject(s_id, s_title))
        
        header_row.addWidget(folder_icon)
        header_row.addWidget(title_label)
        header_row.addWidget(badge)
        header_row.addStretch()
        header_row.addWidget(btn_rename)
        header_row.addWidget(btn_delete)
        
        layout.addLayout(header_row)
        
        # Modules List Container
        modules_layout = QVBoxLayout()
        modules_layout.setSpacing(6)
        
        if not modules:
            no_mods_lbl = QLabel("Empty")
            no_mods_lbl.setStyleSheet("color: #484852; font-size: 12px; padding: 6px 4px;")
            modules_layout.addWidget(no_mods_lbl)
        else:
            for mod in modules:
                mod_row = self.create_module_row(subject_title, mod)
                modules_layout.addWidget(mod_row)
                
        layout.addLayout(modules_layout)
        
        # Bottom Action: Learn all modules
        btn_learn_all = QPushButton("Study")
        btn_learn_all.setObjectName("LearnAllBtn")
        btn_learn_all.setIcon(icons.get_icon("zap", "#ededed", 14))
        btn_learn_all.setFocusPolicy(Qt.NoFocus)
        if total_cards == 0:
            btn_learn_all.setEnabled(False)
        else:
            btn_learn_all.clicked.connect(lambda checked, s_id=subject_id, s_title=subject_title: self.start_subject_session(s_id, s_title))
            
        layout.addWidget(btn_learn_all)
        
        return card

    def create_module_row(self, subject_title: str, mod: dict) -> QFrame:
        row = QFrame()
        row.setObjectName("ModuleRow")
        layout = QHBoxLayout(row)
        layout.setContentsMargins(12, 7, 12, 7)
        layout.setSpacing(10)
        
        mod_id = mod["id"]
        mod_title = mod["title"]
        count = mod["card_count"]
        
        file_icon = QLabel()
        file_icon.setPixmap(icons.get_pixmap("file", "#787882", 14))
        
        lbl_name = QLabel(mod_title)
        lbl_name.setStyleSheet("font-weight: 500; color: #ededed; font-size: 13px;")
        
        lbl_count = QLabel(str(count))
        lbl_count.setStyleSheet("color: #5c5c66; font-size: 12px;")
        
        btn_view = QPushButton("View")
        btn_view.setIcon(icons.get_icon("eye", "#ededed", 12))
        btn_view.setStyleSheet("padding: 5px 12px; font-size: 12px;")
        btn_view.setFocusPolicy(Qt.NoFocus)
        btn_view.clicked.connect(lambda checked, m_id=mod_id: self.open_deck_browser(m_id))

        btn_learn = QPushButton("Study")
        btn_learn.setIcon(icons.get_icon("play", "#ededed", 11))
        btn_learn.setStyleSheet("padding: 5px 12px; font-size: 12px;")
        btn_learn.setFocusPolicy(Qt.NoFocus)
        if count == 0:
            btn_learn.setEnabled(False)
        else:
            btn_learn.clicked.connect(lambda checked, m_id=mod_id, m_title=mod_title, s_title=subject_title: self.start_module_session(m_id, m_title, s_title))
            
        btn_del = QPushButton()
        btn_del.setObjectName("IconBtn")
        btn_del.setIcon(icons.get_icon("trash", "#787882", 13))
        btn_del.setToolTip("Delete")
        btn_del.setFocusPolicy(Qt.NoFocus)
        btn_del.clicked.connect(lambda checked, m_id=mod_id, m_title=mod_title: self.confirm_delete_module(m_id, m_title))
        
        layout.addWidget(file_icon)
        layout.addWidget(lbl_name)
        layout.addWidget(lbl_count)
        layout.addStretch()
        layout.addWidget(btn_view)
        layout.addWidget(btn_learn)
        layout.addWidget(btn_del)
        
        return row

    def prompt_create_subject(self):
        name, ok = QInputDialog.getText(self, "New", "Name:")
        if ok and name.strip():
            database.create_subject(name.strip())
            self.load_subjects_overview()

    def prompt_rename_subject(self, subject_id: int, current_title: str):
        new_name, ok = QInputDialog.getText(self, "Rename", "Name:", text=current_title)
        if ok and new_name.strip():
            database.rename_subject(subject_id, new_name.strip())
            self.load_subjects_overview()

    def confirm_delete_subject(self, subject_id: int, title: str):
        reply = QMessageBox.question(
            self, "Delete",
            f"Delete '{title}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            database.delete_subject(subject_id)
            self.load_subjects_overview()

    def confirm_delete_module(self, module_id: int, title: str):
        reply = QMessageBox.question(
            self, "Delete",
            f"Delete '{title}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            database.delete_module(module_id)
            self.load_subjects_overview()

    # =========================================================================
    # Page 1: Add / AI Generate Module
    # =========================================================================
    def init_add_page(self):
        layout = QVBoxLayout(self.page_add)
        layout.setContentsMargins(40, 32, 40, 32)
        layout.setSpacing(16)
        
        header = QLabel("Add")
        header.setStyleSheet("font-size: 20px; font-weight: 700; color: #ffffff; letter-spacing: -0.4px;")
        layout.addWidget(header)
        layout.addSpacing(4)
        
        # Subject Selector Row
        lbl_subj = QLabel("Subject")
        lbl_subj.setStyleSheet("font-weight: 600; color: #a1a1aa;")
        
        subj_layout = QHBoxLayout()
        self.combo_subjects = QComboBox()
        self.combo_subjects.setMinimumHeight(38)
        
        self.btn_add_subj_inline = QPushButton("+ New")
        self.btn_add_subj_inline.setFixedHeight(38)
        self.btn_add_subj_inline.setFocusPolicy(Qt.NoFocus)
        self.btn_add_subj_inline.clicked.connect(self.prompt_create_subject_inline)
        
        subj_layout.addWidget(self.combo_subjects, stretch=1)
        subj_layout.addWidget(self.btn_add_subj_inline)
        
        layout.addWidget(lbl_subj)
        layout.addLayout(subj_layout)
        
        # Module Title
        lbl_module = QLabel("Module")
        lbl_module.setStyleSheet("font-weight: 600; color: #a1a1aa;")
        self.input_module = QLineEdit()
        self.input_module.setPlaceholderText("Title")
        self.input_module.setMinimumHeight(38)
        
        layout.addWidget(lbl_module)
        layout.addWidget(self.input_module)
        
        # Notes Content
        lbl_notes = QLabel("Notes")
        lbl_notes.setStyleSheet("font-weight: 600; color: #a1a1aa;")
        self.input_notes = QTextEdit()
        self.input_notes.setPlaceholderText("Paste notes...")
        
        layout.addWidget(lbl_notes)
        layout.addWidget(self.input_notes)
        
        # Quota Status Card on Add Page
        self.add_quota_card = QFrame()
        self.add_quota_card.setObjectName("AddQuotaCard")
        add_quota_layout = QVBoxLayout(self.add_quota_card)
        add_quota_layout.setContentsMargins(14, 12, 14, 12)
        add_quota_layout.setSpacing(8)
        
        top_row = QHBoxLayout()
        icon_activity = QLabel()
        icon_activity.setPixmap(icons.get_pixmap("activity", "#82828c", 13))
        
        lbl_quota_head = QLabel("Quota")
        lbl_quota_head.setStyleSheet("font-size: 12px; font-weight: 600; color: #ededed;")
        
        self.lbl_add_quota_nums = QLabel("0 / 50")
        self.lbl_add_quota_nums.setStyleSheet("font-size: 12px; color: #a1a1aa;")
        
        self.btn_edit_quota = QPushButton("Edit")
        self.btn_edit_quota.setObjectName("IconBtn")
        self.btn_edit_quota.setFocusPolicy(Qt.NoFocus)
        self.btn_edit_quota.clicked.connect(self.prompt_edit_quota_limit)
        
        top_row.addWidget(icon_activity)
        top_row.addSpacing(3)
        top_row.addWidget(lbl_quota_head)
        top_row.addStretch()
        top_row.addWidget(self.lbl_add_quota_nums)
        top_row.addSpacing(6)
        top_row.addWidget(self.btn_edit_quota)
        
        self.add_quota_bar = QProgressBar()
        self.add_quota_bar.setRange(0, 100)
        self.add_quota_bar.setFixedHeight(3)
        self.add_quota_bar.setTextVisible(False)
        
        self.lbl_add_quota_sub = QLabel("50 left")
        self.lbl_add_quota_sub.setStyleSheet("font-size: 11.5px; color: #71717a;")
        
        add_quota_layout.addLayout(top_row)
        add_quota_layout.addWidget(self.add_quota_bar)
        add_quota_layout.addWidget(self.lbl_add_quota_sub)
        
        layout.addWidget(self.add_quota_card)
        layout.addSpacing(4)
        
        # Action
        self.btn_generate = QPushButton("Generate")
        self.btn_generate.setObjectName("PrimaryBtn")
        self.btn_generate.setIcon(icons.get_icon("sparkles", "#09090b", 15))
        self.btn_generate.setMinimumHeight(40)
        self.btn_generate.setFocusPolicy(Qt.NoFocus)
        self.btn_generate.clicked.connect(self.process_pasted_notes)
        
        layout.addWidget(self.btn_generate)

    def refresh_add_page_subjects(self):
        self.combo_subjects.clear()
        subjects = database.get_subjects()
        for s in subjects:
            self.combo_subjects.addItem(s['title'], s["id"])
        
        if not subjects:
            self.combo_subjects.addItem("(No subjects)", None)

    def prompt_create_subject_inline(self):
        name, ok = QInputDialog.getText(self, "New", "Name:")
        if ok and name.strip():
            new_id = database.create_subject(name.strip())
            self.refresh_add_page_subjects()
            idx = self.combo_subjects.findData(new_id)
            if idx >= 0:
                self.combo_subjects.setCurrentIndex(idx)

    def process_pasted_notes(self):
        subject_id = self.combo_subjects.currentData()
        subject_title = self.combo_subjects.currentText().strip()
        module_title = self.input_module.text().strip()
        content = self.input_notes.toPlainText().strip()
        
        if not subject_id or not module_title or not content:
            QMessageBox.warning(self, "Missing", "All fields required.")
            return

        modal = GenerationLoadingModal(self, module_title)
        
        def on_view_cards_callback(mod_id):
            self.open_deck_browser(mod_id)

        modal.on_view_cards = on_view_cards_callback

        worker = GenerationWorker(module_title, content)
        self._current_gen_worker = worker

        def on_finished(ai_response):
            try:
                database.save_module_and_cards(subject_title, module_title, content, ai_response, subject_id=subject_id)
                
                # Look up newly created module ID
                modules_data = database.get_subjects_and_modules()
                new_module_id = None
                for s in modules_data:
                    if s["id"] == subject_id:
                        for m in s["modules"]:
                            if m["title"] == module_title:
                                new_module_id = m["id"]
                                break
                                
                self.input_module.clear()
                self.input_notes.clear()
                self.update_quota_display()
                self.load_subjects_overview()
                
                card_count = len(ai_response.cards)
                modal.set_success(card_count, new_module_id)
            except Exception as e:
                modal.set_error(str(e))

        def on_error(err_str):
            self.update_quota_display()
            modal.set_error(err_str)

        worker.finished.connect(on_finished)
        worker.error.connect(on_error)
        worker.start()

        modal.exec()

    def update_quota_display(self):
        stats = database.get_daily_usage_stats()
        used = stats["requests_today"]
        limit = stats["quota_limit"]
        pct = stats["percentage"]
        remaining = stats["remaining"]
        is_exhausted = stats["is_exhausted"]

        if is_exhausted or pct >= 90:
            color = "#f43f5e"
            status_text = "Exhausted" if is_exhausted else "High"
        elif pct >= 70:
            color = "#f59e0b"
            status_text = f"{remaining} left"
        else:
            color = "#10b981"
            status_text = f"{remaining} left"

        bar_style = f"""
            QProgressBar {{
                background-color: #15151f;
                border: none;
                border-radius: 2px;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 2px;
            }}
        """

        # Update Sidebar
        self.lbl_sidebar_quota_val.setText(f"{used} / {limit}")
        self.sidebar_quota_bar.setValue(int(pct))
        self.sidebar_quota_bar.setStyleSheet(bar_style)
        self.lbl_sidebar_quota_status.setText(status_text)
        self.lbl_sidebar_quota_status.setStyleSheet(f"font-size: 10px; color: {color if pct >= 70 else '#63636e'};")

        # Update Add Page
        self.lbl_add_quota_nums.setText(f"{used} / {limit}")
        self.add_quota_bar.setValue(int(pct))
        self.add_quota_bar.setStyleSheet(bar_style)
        self.lbl_add_quota_sub.setText(status_text)
        self.lbl_add_quota_sub.setStyleSheet(f"font-size: 11.5px; color: {color if pct >= 70 else '#71717a'};")

    def prompt_edit_quota_limit(self):
        current_limit = database.get_quota_limit()
        new_limit, ok = QInputDialog.getInt(
            self, "Quota",
            "Daily limit:",
            value=current_limit, minValue=1, maxValue=100000
        )
        if ok and new_limit > 0:
            database.set_quota_limit(new_limit)
            self.update_quota_display()

    def prompt_set_api_key(self):
        dlg = ApiKeyDialog(self)
        dlg.exec()

    # =========================================================================
    # Page 2: Active Review Session & Multi-Priority Adaptive Engine
    # =========================================================================
    def init_review_page(self):
        layout = QVBoxLayout(self.page_review)
        layout.setContentsMargins(40, 24, 40, 24)
        layout.setSpacing(14)
        
        # Header / Status Row
        top_bar = QHBoxLayout()
        top_bar.setSpacing(12)
        
        self.btn_back_overview = QPushButton("Back")
        self.btn_back_overview.setObjectName("IconBtn")
        self.btn_back_overview.setIcon(icons.get_icon("arrow-left", "#82828c", 14))
        self.btn_back_overview.setFocusPolicy(Qt.NoFocus)
        self.btn_back_overview.clicked.connect(lambda: self.switch_page(0))
        
        self.lbl_session_title = QLabel("Review")
        self.lbl_session_title.setStyleSheet("font-size: 13.5px; font-weight: 600; color: #a1a1aa;")
        
        self.lbl_round_badge = QLabel("Round 1")
        self.lbl_round_badge.setStyleSheet("background-color: #12121b; border: 1px solid #1f1f2e; border-radius: 4px; padding: 2px 8px; font-size: 11px; font-weight: 700; color: #818cf8; letter-spacing: 0.5px;")
        
        self.lbl_counter = QLabel("0 / 0")
        self.lbl_counter.setStyleSheet("color: #63636e; font-size: 12px; font-weight: 500;")
        
        top_bar.addWidget(self.btn_back_overview)
        top_bar.addWidget(self.lbl_session_title)
        top_bar.addSpacing(6)
        top_bar.addWidget(self.lbl_round_badge)
        top_bar.addStretch()
        top_bar.addWidget(self.lbl_counter)
        
        # Thin Progress Line
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(3)
        
        # Review Content Area
        review_scroll = QScrollArea()
        review_scroll.setWidgetResizable(True)
        review_scroll.setFrameShape(QFrame.NoFrame)
        review_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_content = QWidget()
        scroll_content.setObjectName("ScrollContainer")
        content_vbox = QVBoxLayout(scroll_content)
        content_vbox.setSpacing(18)
        content_vbox.setContentsMargins(0, 12, 0, 24)
        content_vbox.addStretch(1)
        
        # Card Container
        card_hbox = QHBoxLayout()
        card_hbox.addStretch()
        
        self.card_frame = QFrame()
        self.card_frame.setObjectName("ReviewCard")
        self.card_frame.setFixedWidth(760)
        
        card_layout = QVBoxLayout(self.card_frame)
        card_layout.setContentsMargins(36, 30, 36, 32)
        card_layout.setSpacing(16)
        
        # Card Header: Concept Tag + Pos
        card_top = QHBoxLayout()
        self.lbl_card_concept = QLabel("CONCEPT")
        self.lbl_card_concept.setStyleSheet("color: #63636e; font-size: 10.5px; font-weight: 700; letter-spacing: 1.4px;")
        
        self.lbl_card_pos = QLabel("1 / 1")
        self.lbl_card_pos.setStyleSheet("color: #52525b; font-size: 12px; font-weight: 500;")
        
        card_top.addWidget(self.lbl_card_concept)
        card_top.addStretch()
        card_top.addWidget(self.lbl_card_pos)
        
        # Question
        self.lbl_card_question = QLabel("")
        self.lbl_card_question.setStyleSheet("font-size: 20px; font-weight: 600; color: #fafafa; line-height: 1.5; padding: 6px 0;")
        self.lbl_card_question.setWordWrap(True)
        
        # Answer Container
        self.answer_container = QWidget()
        answer_layout = QVBoxLayout(self.answer_container)
        answer_layout.setContentsMargins(0, 8, 0, 0)
        answer_layout.setSpacing(10)
        
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet("background-color: #1a1a2e; max-height: 1px; border: none;")
        
        self.lbl_card_explanation = QLabel("")
        self.lbl_card_explanation.setTextFormat(Qt.RichText)
        self.lbl_card_explanation.setWordWrap(True)
        self.lbl_card_explanation.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.lbl_card_explanation.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.lbl_card_explanation.setStyleSheet(
            "QLabel { background: transparent; border: none; padding: 0; }"
        )
        
        self.mem_row_widget = QWidget()
        mem_row_layout = QHBoxLayout(self.mem_row_widget)
        mem_row_layout.setContentsMargins(0, 2, 0, 0)
        mem_row_layout.setSpacing(6)
        
        mem_label_head = QLabel("CODE")
        mem_label_head.setStyleSheet(
            "color: #52525b; font-size: 9.5px; font-weight: 700; letter-spacing: 1px;"
        )
        
        self.lbl_card_memory = QLabel("")
        self.lbl_card_memory.setTextFormat(Qt.RichText)
        self.lbl_card_memory.setStyleSheet(
            "QLabel { background: transparent; border: none; padding: 0; }"
        )
        
        mem_row_layout.addWidget(mem_label_head)
        mem_row_layout.addWidget(self.lbl_card_memory)
        mem_row_layout.addStretch()
        
        answer_layout.addWidget(divider)
        answer_layout.addWidget(self.lbl_card_explanation)
        answer_layout.addWidget(self.mem_row_widget)
        self.answer_container.hide()
        
        card_layout.addLayout(card_top)
        card_layout.addWidget(self.lbl_card_question)
        card_layout.addWidget(self.answer_container)
        card_layout.addStretch()
        
        # Completion Container
        self.completion_container = QWidget()
        self.completion_container.setFixedWidth(760)
        comp_layout = QVBoxLayout(self.completion_container)
        comp_layout.setAlignment(Qt.AlignCenter)
        comp_layout.setSpacing(14)
        
        lbl_comp_badge = QLabel("COMPLETE")
        lbl_comp_badge.setStyleSheet("color: #10b981; font-size: 11px; font-weight: 800; letter-spacing: 1.8px;")
        lbl_comp_badge.setAlignment(Qt.AlignCenter)
        
        self.lbl_comp_title = QLabel("Mastered")
        self.lbl_comp_title.setStyleSheet("font-size: 24px; font-weight: 700; color: #ffffff;")
        self.lbl_comp_title.setAlignment(Qt.AlignCenter)
        
        self.lbl_comp_stats = QLabel("")
        self.lbl_comp_stats.setStyleSheet("color: #71717a; font-size: 13.5px;")
        self.lbl_comp_stats.setAlignment(Qt.AlignCenter)
        
        comp_btn_row = QHBoxLayout()
        comp_btn_row.setAlignment(Qt.AlignCenter)
        comp_btn_row.setSpacing(12)
        
        btn_restart = QPushButton("Restart")
        btn_restart.setObjectName("PrimaryBtn")
        btn_restart.setIcon(icons.get_icon("refresh", "#09090b", 13))
        btn_restart.setFocusPolicy(Qt.NoFocus)
        btn_restart.clicked.connect(self.restart_current_session)
        
        btn_return = QPushButton("Back")
        btn_return.setFocusPolicy(Qt.NoFocus)
        btn_return.clicked.connect(lambda: self.switch_page(0))
        
        comp_btn_row.addWidget(btn_restart)
        comp_btn_row.addWidget(btn_return)
        
        comp_layout.addStretch()
        comp_layout.addWidget(lbl_comp_badge)
        comp_layout.addWidget(self.lbl_comp_title)
        comp_layout.addWidget(self.lbl_comp_stats)
        comp_layout.addSpacing(8)
        comp_layout.addLayout(comp_btn_row)
        comp_layout.addStretch()
        
        self.completion_container.hide()
        
        card_hbox.addWidget(self.card_frame)
        card_hbox.addWidget(self.completion_container)
        card_hbox.addStretch()
        
        # Action Controls Container
        controls_hbox = QHBoxLayout()
        controls_hbox.addStretch()
        
        self.controls_widget = QWidget()
        self.controls_widget.setFixedWidth(760)
        controls_layout = QVBoxLayout(self.controls_widget)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(10)
        
        # Reveal Button
        self.btn_reveal = QPushButton("Reveal")
        self.btn_reveal.setObjectName("RevealActionBtn")
        self.btn_reveal.setFixedHeight(44)
        self.btn_reveal.setFocusPolicy(Qt.NoFocus)
        self.btn_reveal.clicked.connect(self.reveal_card_answer)
        
        # 3 Rating Buttons — one word each
        self.rating_widget = QWidget()
        rating_layout = QHBoxLayout(self.rating_widget)
        rating_layout.setContentsMargins(0, 0, 0, 0)
        rating_layout.setSpacing(12)
        
        self.btn_rate_didnt_know = QPushButton("Again")
        self.btn_rate_didnt_know.setObjectName("RateDidntKnow")
        self.btn_rate_didnt_know.setFixedHeight(44)
        self.btn_rate_didnt_know.setFocusPolicy(Qt.NoFocus)
        self.btn_rate_didnt_know.clicked.connect(lambda: self.rate_active_card("Didn't know"))
        
        self.btn_rate_abit = QPushButton("Hard")
        self.btn_rate_abit.setObjectName("RateABit")
        self.btn_rate_abit.setFixedHeight(44)
        self.btn_rate_abit.setFocusPolicy(Qt.NoFocus)
        self.btn_rate_abit.clicked.connect(lambda: self.rate_active_card("A bit"))
        
        self.btn_rate_iknow = QPushButton("Easy")
        self.btn_rate_iknow.setObjectName("RateIKnow")
        self.btn_rate_iknow.setFixedHeight(44)
        self.btn_rate_iknow.setFocusPolicy(Qt.NoFocus)
        self.btn_rate_iknow.clicked.connect(lambda: self.rate_active_card("I know"))
        
        rating_layout.addWidget(self.btn_rate_didnt_know)
        rating_layout.addWidget(self.btn_rate_abit)
        rating_layout.addWidget(self.btn_rate_iknow)
        self.rating_widget.hide()
        
        controls_layout.addWidget(self.btn_reveal)
        controls_layout.addWidget(self.rating_widget)
        
        controls_hbox.addWidget(self.controls_widget)
        controls_hbox.addStretch()
        
        content_vbox.addLayout(card_hbox)
        content_vbox.addLayout(controls_hbox)
        content_vbox.addStretch(1)
        
        review_scroll.setWidget(scroll_content)
        
        layout.addLayout(top_bar)
        layout.addWidget(self.progress_bar)
        layout.addWidget(review_scroll, stretch=1)

    def start_module_session(self, module_id: int, module_title: str, subject_title: str):
        cards = database.get_cards_for_module(module_id)
        if not cards:
            QMessageBox.information(self, "Empty", "No cards.")
            return
        
        session_title = f"{subject_title} / {module_title}"
        self.current_session = ReviewSession(title=session_title, cards=cards)
        self.switch_page(2)
        self.render_session_card()

    def start_subject_session(self, subject_id: int, subject_title: str):
        cards = database.get_cards_for_subject(subject_id)
        if not cards:
            QMessageBox.information(self, "Empty", "No cards.")
            return
            
        session_title = f"{subject_title}"
        self.current_session = ReviewSession(title=session_title, cards=cards)
        self.switch_page(2)
        self.render_session_card()

    def render_session_card(self):
        if not self.current_session:
            return

        session = self.current_session
        self.lbl_session_title.setText(session.title)
        self.lbl_round_badge.setText(f"Round {session.round_number}")
        
        if session.is_completed:
            self.card_frame.hide()
            self.controls_widget.hide()
            self.completion_container.show()
            
            self.lbl_counter.setText("Done")
            self.progress_bar.setValue(100)
            self.lbl_comp_stats.setText(
                f"{session.initial_total} cards • {session.round_number} rounds"
            )
            return

        self.completion_container.hide()
        self.card_frame.show()
        self.controls_widget.show()
        
        card = session.current_card
        if not card:
            return
            
        self.lbl_counter.setText(
            f"{session.remaining_count} / {session.initial_total}"
        )
        self.lbl_card_pos.setText(
            f"{session.round_card_number} / {session.round_total_cards}"
        )
        self.progress_bar.setValue(int(session.progress_percentage))
        
        self.lbl_card_concept.setText(card.get("concept_group", "CONCEPT").upper())
        self.lbl_card_question.setText(card.get("question", ""))
        
        explanation = card.get("explanation", "")
        explanation_html = format_explanation_html(explanation)
        self.lbl_card_explanation.setText(explanation_html)
        
        memory_code = card.get("memory_code", "") or ""
        if memory_code.strip():
            pills = "".join(
                f'<span style="'
                f'display:inline-block; '
                f'background:#0f2437; border:1px solid #1e4976; border-radius:5px; '
                f'color:#38bdf8; font-size:12px; font-weight:800; '
                f'padding:1px 7px; margin-right:3px;">'
                f'{c}</span>'
                for c in memory_code.strip()
            )
            self.lbl_card_memory.setText(pills)
            self.mem_row_widget.show()
        else:
            self.mem_row_widget.hide()
            
        self.is_card_revealed = False
        self.answer_container.hide()
        self.btn_reveal.show()
        self.rating_widget.hide()

    def reveal_card_answer(self):
        if not self.current_session or self.current_session.is_completed:
            return
        self.is_card_revealed = True
        self.answer_container.show()
        self.btn_reveal.hide()
        self.rating_widget.show()

    def rate_active_card(self, rating: str):
        if not self.current_session or not self.is_card_revealed:
            return

        card = self.current_session.current_card
        if card:
            database.update_card_state(card["id"], rating)

        self.current_session.record_rating(rating)
        self.render_session_card()

    def restart_current_session(self):
        if self.current_session:
            self.current_session.restart()
            self.render_session_card()

    # =========================================================================
    # Page 3: Deck Browser & Card Manager (Scrollable, View, Add, Edit, Delete)
    # =========================================================================
    def init_deck_page(self):
        layout = QVBoxLayout(self.page_deck)
        layout.setContentsMargins(40, 24, 40, 24)
        layout.setSpacing(16)
        
        # Header Row
        top_bar = QHBoxLayout()
        top_bar.setSpacing(12)
        
        btn_back = QPushButton("Back")
        btn_back.setObjectName("IconBtn")
        btn_back.setIcon(icons.get_icon("arrow-left", "#82828c", 14))
        btn_back.setFocusPolicy(Qt.NoFocus)
        btn_back.clicked.connect(lambda: self.switch_page(0))
        
        title_box = QVBoxLayout()
        title_box.setSpacing(2)
        
        self.lbl_deck_breadcrumb = QLabel("")
        self.lbl_deck_breadcrumb.setStyleSheet("font-size: 11px; font-weight: 700; color: #818cf8; letter-spacing: 0.5px;")
        
        self.lbl_deck_title = QLabel("Cards")
        self.lbl_deck_title.setStyleSheet("font-size: 20px; font-weight: 700; color: #ffffff; letter-spacing: -0.4px;")
        
        title_box.addWidget(self.lbl_deck_breadcrumb)
        title_box.addWidget(self.lbl_deck_title)
        
        self.lbl_deck_count_badge = QLabel("0")
        self.lbl_deck_count_badge.setStyleSheet("background-color: #12121b; border: 1px solid #1f1f2e; border-radius: 4px; padding: 3px 9px; font-size: 11.5px; font-weight: 600; color: #818cf8;")
        
        self.btn_deck_add_card = QPushButton("+ Add")
        self.btn_deck_add_card.setObjectName("PrimaryBtn")
        self.btn_deck_add_card.setFocusPolicy(Qt.NoFocus)
        self.btn_deck_add_card.clicked.connect(self.prompt_add_card_in_deck)
        
        self.btn_deck_study = QPushButton("Study")
        self.btn_deck_study.setIcon(icons.get_icon("play", "#ffffff", 12))
        self.btn_deck_study.setFocusPolicy(Qt.NoFocus)
        self.btn_deck_study.setStyleSheet("background-color: #161622; border: 1px solid #28283c; padding: 7px 14px; font-weight: 600; color: #ededed;")
        self.btn_deck_study.clicked.connect(self.start_study_from_deck)
        
        top_bar.addWidget(btn_back)
        top_bar.addLayout(title_box)
        top_bar.addSpacing(6)
        top_bar.addWidget(self.lbl_deck_count_badge)
        top_bar.addStretch()
        top_bar.addWidget(self.btn_deck_add_card)
        top_bar.addWidget(self.btn_deck_study)
        
        # Search Bar
        filter_bar = QHBoxLayout()
        self.input_deck_search = QLineEdit()
        self.input_deck_search.setObjectName("SearchInput")
        self.input_deck_search.setPlaceholderText("Search...")
        self.input_deck_search.textChanged.connect(self.filter_deck_cards)
        
        filter_bar.addWidget(self.input_deck_search)
        
        # Scroll Area for Cards Feed
        self.deck_scroll = QScrollArea()
        self.deck_scroll.setWidgetResizable(True)
        self.deck_scroll.setFrameShape(QFrame.NoFrame)
        self.deck_container = QWidget()
        self.deck_container.setObjectName("DeckContainer")
        self.deck_layout = QVBoxLayout(self.deck_container)
        self.deck_layout.setContentsMargins(0, 8, 12, 24)
        self.deck_layout.setSpacing(14)
        self.deck_layout.addStretch()
        
        self.deck_scroll.setWidget(self.deck_container)
        
        layout.addLayout(top_bar)
        layout.addLayout(filter_bar)
        layout.addWidget(self.deck_scroll)

    def open_deck_browser(self, module_id: int):
        self.current_deck_module_id = module_id
        self.input_deck_search.clear()
        self.load_deck_for_module(module_id)
        self.switch_page(3)

    def load_deck_for_module(self, module_id: int):
        self.current_deck_module_id = module_id
        mod_info = database.get_module_by_id(module_id)
        cards = database.get_cards_for_module(module_id)
        self.current_deck_cards = cards
        
        if mod_info:
            sub_title = mod_info.get("subject_title") or ""
            self.lbl_deck_breadcrumb.setText(sub_title.upper())
            self.lbl_deck_title.setText(mod_info["title"])
        else:
            self.lbl_deck_breadcrumb.setText("")
            self.lbl_deck_title.setText("Cards")
            
        count = len(cards)
        self.lbl_deck_count_badge.setText(str(count))
        self.btn_deck_study.setEnabled(count > 0)
        
        # Clear layout (preserve trailing stretch)
        while self.deck_layout.count() > 1:
            child = self.deck_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        self.deck_card_widgets.clear()
        
        if not cards:
            empty_box = QWidget()
            eb_layout = QVBoxLayout(empty_box)
            eb_layout.setAlignment(Qt.AlignCenter)
            eb_layout.setSpacing(12)
            eb_layout.setContentsMargins(0, 48, 0, 48)
            
            lbl_empty = QLabel("Empty")
            lbl_empty.setStyleSheet("color: #71717a; font-size: 14px;")
            lbl_empty.setAlignment(Qt.AlignCenter)
            
            btn_add_first = QPushButton("+ Add")
            btn_add_first.setObjectName("PrimaryBtn")
            btn_add_first.setFixedWidth(140)
            btn_add_first.setFocusPolicy(Qt.NoFocus)
            btn_add_first.clicked.connect(self.prompt_add_card_in_deck)
            
            eb_layout.addWidget(lbl_empty)
            eb_layout.addWidget(btn_add_first, 0, Qt.AlignCenter)
            self.deck_layout.insertWidget(0, empty_box)
            return

        for idx, card in enumerate(cards):
            card_widget = self.create_deck_card_widget(card, idx + 1)
            self.deck_card_widgets.append((card_widget, card))
            self.deck_layout.insertWidget(idx, card_widget)

    def create_deck_card_widget(self, card: dict, card_number: int) -> QFrame:
        card_id = card["id"]
        frame = QFrame()
        frame.setObjectName("DeckCardItem")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(22, 18, 22, 18)
        layout.setSpacing(12)
        
        # Top Meta Row
        top_row = QHBoxLayout()
        top_row.setSpacing(8)
        
        num_badge = QLabel(f"#{card_number}")
        num_badge.setStyleSheet("color: #71717a; font-size: 11px; font-weight: 700; background-color: #12121a; border: 1px solid #1a1a28; border-radius: 4px; padding: 2px 6px;")
        
        concept = card.get("concept_group", "CONCEPT").strip().upper()
        concept_badge = QLabel(concept)
        concept_badge.setStyleSheet("color: #38bdf8; font-size: 11px; font-weight: 700; background-color: #0c1a29; border: 1px solid #163b5c; border-radius: 4px; padding: 2px 8px; letter-spacing: 0.5px;")
        
        state = card.get("review_state", "Didn_know")
        if state == "I know":
            state_pill = QLabel("Mastered")
            state_pill.setStyleSheet("color: #34d399; font-size: 10.5px; font-weight: 600; background-color: #06281e; border: 1px solid #065f46; border-radius: 4px; padding: 2px 7px;")
        elif state == "A bit":
            state_pill = QLabel("Reviewing")
            state_pill.setStyleSheet("color: #fbbf24; font-size: 10.5px; font-weight: 600; background-color: #291807; border: 1px solid #78350f; border-radius: 4px; padding: 2px 7px;")
        else:
            state_pill = QLabel("New")
            state_pill.setStyleSheet("color: #71717a; font-size: 10.5px; font-weight: 500; background-color: #14141c; border: 1px solid #20202e; border-radius: 4px; padding: 2px 7px;")
            
        btn_edit = QPushButton("Edit")
        btn_edit.setObjectName("IconBtn")
        btn_edit.setIcon(icons.get_icon("edit", "#787882", 13))
        btn_edit.setFocusPolicy(Qt.NoFocus)
        btn_edit.clicked.connect(lambda checked, c_id=card_id: self.prompt_edit_card_in_deck(c_id))
        
        btn_del = QPushButton("Delete")
        btn_del.setObjectName("IconBtnDanger")
        btn_del.setIcon(icons.get_icon("trash", "#787882", 13))
        btn_del.setFocusPolicy(Qt.NoFocus)
        btn_del.clicked.connect(lambda checked, c_id=card_id: self.confirm_delete_card_in_deck(c_id))
        
        top_row.addWidget(num_badge)
        top_row.addWidget(concept_badge)
        top_row.addWidget(state_pill)
        top_row.addStretch()
        top_row.addWidget(btn_edit)
        top_row.addWidget(btn_del)
        
        # Question Label
        q_label = QLabel(card.get("question", ""))
        q_label.setStyleSheet("font-size: 15px; font-weight: 600; color: #f4f4f5; line-height: 1.4;")
        q_label.setWordWrap(True)
        
        # Answer / Bullets
        exp_label = QLabel()
        exp_label.setTextFormat(Qt.RichText)
        exp_label.setWordWrap(True)
        exp_label.setStyleSheet("background: transparent; border: none; padding: 0;")
        exp_html = format_explanation_html(card.get("explanation", ""))
        exp_label.setText(exp_html)
        
        layout.addLayout(top_row)
        layout.addWidget(q_label)
        layout.addWidget(exp_label)
        
        # Memory code pill if available
        mem_code = card.get("memory_code", "") or ""
        if mem_code.strip():
            mem_row = QHBoxLayout()
            mem_row.setSpacing(6)
            lbl_mem_head = QLabel("CODE:")
            lbl_mem_head.setStyleSheet("color: #52525b; font-size: 9.5px; font-weight: 700; letter-spacing: 0.8px;")
            
            pills = "".join(
                f'<span style="background:#0f2437; border:1px solid #1e4976; border-radius:4px; color:#38bdf8; font-size:11px; font-weight:800; padding:1px 6px; margin-right:3px;">{c}</span>'
                for c in mem_code.strip()
            )
            lbl_pills = QLabel(pills)
            lbl_pills.setTextFormat(Qt.RichText)
            
            mem_row.addWidget(lbl_mem_head)
            mem_row.addWidget(lbl_pills)
            mem_row.addStretch()
            layout.addLayout(mem_row)
            
        return frame

    def filter_deck_cards(self, text: str):
        query = text.strip().lower()
        visible_count = 0
        for widget, card in self.deck_card_widgets:
            q = card.get("question", "").lower()
            cg = card.get("concept_group", "").lower()
            exp = card.get("explanation", "").lower()
            mem = (card.get("memory_code", "") or "").lower()
            matches = (query in q) or (query in cg) or (query in exp) or (query in mem)
            widget.setVisible(matches)
            if matches:
                visible_count += 1
                
        self.lbl_deck_count_badge.setText(
            f"{visible_count} / {len(self.deck_card_widgets)}" if query else str(len(self.deck_card_widgets))
        )

    def prompt_add_card_in_deck(self):
        if not self.current_deck_module_id:
            return
        dialog = FlashcardEditDialog(self, is_new=True)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            database.create_flashcard(
                self.current_deck_module_id,
                concept_group=data["concept_group"],
                question=data["question"],
                explanation=data["explanation"],
                memory_code=data["memory_code"]
            )
            self.load_deck_for_module(self.current_deck_module_id)
            self.load_subjects_overview()

    def prompt_edit_card_in_deck(self, card_id: int):
        card = database.get_card_by_id(card_id)
        if not card:
            return
        dialog = FlashcardEditDialog(self, card_data=card, is_new=False)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            database.update_flashcard(
                card_id,
                concept_group=data["concept_group"],
                question=data["question"],
                explanation=data["explanation"],
                memory_code=data["memory_code"]
            )
            self.load_deck_for_module(self.current_deck_module_id)

    def confirm_delete_card_in_deck(self, card_id: int):
        reply = QMessageBox.question(
            self, "Delete",
            "Delete flashcard?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            database.delete_flashcard(card_id)
            self.load_deck_for_module(self.current_deck_module_id)
            self.load_subjects_overview()

    def start_study_from_deck(self):
        if not self.current_deck_module_id:
            return
        mod_info = database.get_module_by_id(self.current_deck_module_id)
        if mod_info:
            sub_title = mod_info.get("subject_title") or "Subject"
            self.start_module_session(self.current_deck_module_id, mod_info["title"], sub_title)

    # --- Keyboard Shortcut Handlers ---
    def on_space_pressed(self):
        """Dedicated Space handler: only reveals answer when on Review page and unrevealed."""
        if self.stack.currentIndex() == 2 and self.current_session and not self.current_session.is_completed:
            if not self.is_card_revealed:
                self.reveal_card_answer()

    def on_number_rating(self, rating: str):
        """Dedicated rating handler: only rates when card is revealed."""
        if self.stack.currentIndex() == 2 and self.current_session and not self.current_session.is_completed:
            if self.is_card_revealed:
                self.rate_active_card(rating)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(MATTE_THEME)
    
    splash = SplashScreen()
    splash.show()
    
    window = None
    def run_main():
        global window
        window = FlasedApp()
        window.show()
        splash.finish(window)

    QTimer.singleShot(900, run_main)
    sys.exit(app.exec())