"""
ui.py - Mark XLVIII PyQt6 Interface with Voice Orb Integration

Complete UI with:
- Voice Orb (audio-reactive particle visualization)
- Conversation log panel
- Waveform display
- Camera feed
- Interrupt button
- System status indicators
- Remote control integration

REQUIRES: pip install PyQt6 PyOpenGL numpy
"""

import sys
import asyncio
from pathlib import Path
from datetime import datetime
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QFrame, QSplitter,
    QStatusBar, QMenuBar, QMenu, QSystemTrayIcon,
    QApplication, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt6.QtGui import QAction, QFont, QIcon, QColor, QPalette

# Import Voice Orb
try:
    from voice_orb import VoiceOrb
    VOICE_ORB_AVAILABLE = True
except ImportError:
    VOICE_ORB_AVAILABLE = False
    print("[UI] Voice orb not available - install with: pip install PyQt6 PyOpenGL numpy")


# ═══════════════════════════════════════════════════════════════
# STYLING
# ═══════════════════════════════════════════════════════════════

DARK_THEME = """
QMainWindow {
    background-color: #071018;
}
QWidget {
    background-color: #071018;
    color: #e6f7fb;
    font-family: 'Segoe UI', Arial, sans-serif;
}
QLabel {
    color: #e6f7fb;
    background: transparent;
}
QTextEdit {
    background-color: #0d1c27;
    color: #e6f7fb;
    border: 1px solid #1d3c4a;
    border-radius: 8px;
    padding: 10px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 12px;
}
QPushButton {
    background-color: #0d1c27;
    color: #e6f7fb;
    border: 1px solid #1d3c4a;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: bold;
    min-height: 20px;
}
QPushButton:hover {
    background-color: #1d3c4a;
    border-color: #00d4ff;
}
QPushButton:pressed {
    background-color: #00d4ff;
    color: #00141b;
}
QPushButton#interruptBtn {
    background-color: #f87171;
    color: white;
    border: 1px solid #dc2626;
}
QPushButton#interruptBtn:hover {
    background-color: #dc2626;
}
QFrame#separator {
    background-color: #1d3c4a;
    max-height: 1px;
}
QStatusBar {
    background-color: #0d1c27;
    color: #9bb6bd;
    border-top: 1px solid #1d3c4a;
}
QMenuBar {
    background-color: #0d1c27;
    color: #e6f7fb;
    border-bottom: 1px solid #1d3c4a;
}
QMenuBar::item:selected {
    background-color: #1d3c4a;
}
QMenu {
    background-color: #0d1c27;
    color: #e6f7fb;
    border: 1px solid #1d3c4a;
}
QMenu::item:selected {
    background-color: #00d4ff;
    color: #00141b;
}
"""


# ═══════════════════════════════════════════════════════════════
# MAIN WINDOW
# ═══════════════════════════════════════════════════════════════

class JarvisUI(QMainWindow):
    """Main JARVIS interface with voice orb integration."""
    
    # Signals for thread-safe UI updates
    log_signal = pyqtSignal(str, str)  # speaker, message
    state_signal = pyqtSignal(str)     # state
    status_signal = pyqtSignal(str)    # status message
    
    def __init__(self, jarvis_instance=None):
        super().__init__()
        self.jarvis = jarvis_instance
        self.setWindowTitle("JARVIS - Mark XLVIII")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # Apply dark theme
        self.setStyleSheet(DARK_THEME)
        
        # Setup UI
        self._setup_ui()
        self._setup_menu()
        self._setup_status_bar()
        self._setup_tray()
        
        # Connect signals
        self.log_signal.connect(self._append_log)
        self.state_signal.connect(self._update_state)
        self.status_signal.connect(self._update_status)
        
        # Initial state
        self.current_state = "idle"
        self._update_state("idle")
        
        # Welcome message
        self._append_log("system", "JARVIS Mark XLVIII initialized")
        self._append_log("system", "Voice Orb: " + ("ACTIVE" if VOICE_ORB_AVAILABLE else "NOT AVAILABLE"))
        self._append_log("jarvis", "Good day. All systems operational. How may I assist you?")
    
    def _setup_ui(self):
        """Setup the main UI layout."""
        central = QWidget()
        self.setCentralWidget(central)
        
        # Main layout
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # ═══ TOP SECTION: Voice Orb + Status ═══
        top_section = QHBoxLayout()
        top_section.setSpacing(20)
        
        # Voice Orb
        if VOICE_ORB_AVAILABLE:
            orb_container = QFrame()
            orb_container.setStyleSheet("""
                QFrame {
                    background-color: #0d1c27;
                    border: 1px solid #1d3c4a;
                    border-radius: 12px;
                }
            """)
            orb_layout = QVBoxLayout(orb_container)
            orb_layout.setContentsMargins(10, 10, 10, 10)
            
            # Title
            orb_title = QLabel("VOICE ORB")
            orb_title.setStyleSheet("color: #9bb6bd; font-size: 11px; font-weight: bold;")
            orb_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            orb_layout.addWidget(orb_title)
            
            # The orb itself
            self.voice_orb = VoiceOrb(self)
            self.voice_orb.setMinimumSize(300, 300)
            self.voice_orb.setMaximumSize(400, 400)
            orb_layout.addWidget(self.voice_orb)
            
            # State label
            self.orb_state_label = QLabel("IDLE")
            self.orb_state_label.setStyleSheet("""
                color: #00d4ff;
                font-size: 14px;
                font-weight: bold;
                padding: 5px;
                background-color: #071018;
                border-radius: 6px;
            """)
            self.orb_state_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            orb_layout.addWidget(self.orb_state_label)
            
            top_section.addWidget(orb_container)
        else:
            # Placeholder when voice orb not available
            placeholder = QLabel("Voice Orb Not Available\nInstall: pip install PyQt6 PyOpenGL numpy")
            placeholder.setStyleSheet("""
                color: #9bb6bd;
                background-color: #0d1c27;
                border: 1px solid #1d3c4a;
                border-radius: 12px;
                padding: 20px;
                font-size: 14px;
            """)
            placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            placeholder.setMinimumSize(300, 300)
            top_section.addWidget(placeholder)
        
        # Status panel (right side)
        status_panel = QFrame()
        status_panel.setStyleSheet("""
            QFrame {
                background-color: #0d1c27;
                border: 1px solid #1d3c4a;
                border-radius: 12px;
            }
        """)
        status_layout = QVBoxLayout(status_panel)
        status_layout.setContentsMargins(15, 15, 15, 15)
        
        # System status title
        status_title = QLabel("SYSTEM STATUS")
        status_title.setStyleSheet("color: #9bb6bd; font-size: 11px; font-weight: bold;")
        status_layout.addWidget(status_title)
        
        # Status indicators
        self.status_indicators = {}
        for name, color in [
            ("Gemini API", "#00d4ff"),
            ("Microphone", "#7ef0c1"),
            ("Web Search", "#fbbf24"),
            ("File System", "#f87171"),
            ("Memory", "#00d4ff"),
            ("Network", "#7ef0c1"),
        ]:
            row = QHBoxLayout()
            indicator = QLabel("●")
            indicator.setStyleSheet(f"color: {color}; font-size: 16px;")
            label = QLabel(name)
            label.setStyleSheet("color: #e6f7fb; font-size: 13px;")
            row.addWidget(indicator)
            row.addWidget(label)
            row.addStretch()
            status_layout.addLayout(row)
            self.status_indicators[name] = indicator
        
        status_layout.addStretch()
        
        # Interrupt button
        self.interrupt_btn = QPushButton("⬛ INTERRUPT")
        self.interrupt_btn.setObjectName("interruptBtn")
        self.interrupt_btn.setMinimumHeight(50)
        self.interrupt_btn.clicked.connect(self._on_interrupt)
        status_layout.addWidget(self.interrupt_btn)
        
        # Remote control button
        self.remote_btn = QPushButton("📱 REMOTE CONTROL")
        self.remote_btn.setMinimumHeight(40)
        self.remote_btn.clicked.connect(self._on_remote_control)
        status_layout.addWidget(self.remote_btn)
        
        top_section.addWidget(status_panel)
        main_layout.addLayout(top_section)
        
        # ═══ MIDDLE SECTION: Conversation Log ═══
        log_frame = QFrame()
        log_frame.setStyleSheet("""
            QFrame {
                background-color: #0d1c27;
                border: 1px solid #1d3c4a;
                border-radius: 12px;
            }
        """)
        log_layout = QVBoxLayout(log_frame)
        log_layout.setContentsMargins(15, 15, 15, 15)
        
        # Log header
        log_header = QHBoxLayout()
        log_title = QLabel("CONVERSATION LOG")
        log_title.setStyleSheet("color: #9bb6bd; font-size: 11px; font-weight: bold;")
        log_header.addWidget(log_title)
        log_header.addStretch()
        
        clear_btn = QPushButton("Clear")
        clear_btn.setMaximumWidth(80)
        clear_btn.clicked.connect(self._clear_log)
        log_header.addWidget(clear_btn)
        
        log_layout.addLayout(log_header)
        
        # Log text area
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMinimumHeight(300)
        log_layout.addWidget(self.log_text)
        
        main_layout.addWidget(log_frame)
        
        # ═══ BOTTOM SECTION: Quick Actions ═══
        actions_frame = QFrame()
        actions_frame.setStyleSheet("""
            QFrame {
                background-color: #0d1c27;
                border: 1px solid #1d3c4a;
                border-radius: 12px;
            }
        """)
        actions_layout = QHBoxLayout(actions_frame)
        actions_layout.setContentsMargins(15, 15, 15, 15)
        
        # Quick action buttons
        quick_actions = [
            ("🔍 Search", self._on_search),
            ("📁 Files", self._on_files),
            ("🌤️ Weather", self._on_weather),
            ("📰 News", self._on_news),
            ("🎵 Music", self._on_music),
            ("⚙️ Settings", self._on_settings),
        ]
        
        for text, callback in quick_actions:
            btn = QPushButton(text)
            btn.clicked.connect(callback)
            actions_layout.addWidget(btn)
        
        main_layout.addWidget(actions_frame)
    
    def _setup_menu(self):
        """Setup menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_session = QAction("New Session", self)
        new_session.setShortcut("Ctrl+N")
        new_session.triggered.connect(self._new_session)
        file_menu.addAction(new_session)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        toggle_orb = QAction("Toggle Voice Orb", self)
        toggle_orb.triggered.connect(self._toggle_orb)
        view_menu.addAction(toggle_orb)
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        
        memory_action = QAction("View Memory", self)
        memory_action.triggered.connect(self._view_memory)
        tools_menu.addAction(memory_action)
        
        logs_action = QAction("View Logs", self)
        logs_action.triggered.connect(self._view_logs)
        tools_menu.addAction(logs_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _setup_status_bar(self):
        """Setup status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        self.status_label = QLabel("Ready")
        self.status_bar.addWidget(self.status_label)
        
        self.time_label = QLabel()
        self.status_bar.addPermanentWidget(self.time_label)
        
        # Update time every second
        self.time_timer = QTimer(self)
        self.time_timer.timeout.connect(self._update_time)
        self.time_timer.start(1000)
        self._update_time()
    
    def _setup_tray(self):
        """Setup system tray icon."""
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray = QSystemTrayIcon(self)
            # Note: You'd need an actual icon file here
            # self.tray.setIcon(QIcon("jarvis.ico"))
            
            tray_menu = QMenu()
            show_action = tray_menu.addAction("Show")
            show_action.triggered.connect(self.show)
            
            quit_action = tray_menu.addAction("Quit")
            quit_action.triggered.connect(QApplication.instance().quit)
            
            self.tray.setContextMenu(tray_menu)
            self.tray.show()
    
    # ═══════════════════════════════════════════════════════════════
    # PUBLIC METHODS (called from main.py)
    # ═══════════════════════════════════════════════════════════════
    
    def write_log(self, speaker: str, message: str):
        """Thread-safe log writing."""
        self.log_signal.emit(speaker, message)
    
    def set_state(self, state: str):
        """Set JARVIS state (idle, listening, thinking, speaking)."""
        self.state_signal.emit(state)
    
    def set_status(self, message: str):
        """Set status bar message."""
        self.status_signal.emit(message)
    
    def set_audio_bands(self, low: float, mid: float, high: float):
        """Update voice orb with audio data."""
        if VOICE_ORB_AVAILABLE and hasattr(self, 'voice_orb'):
            self.voice_orb.set_audio(low, mid, high)
    
    # ═══════════════════════════════════════════════════════════════
    # PRIVATE METHODS
    # ═══════════════════════════════════════════════════════════════
    
    def _append_log(self, speaker: str, message: str):
        """Append a log entry to the conversation log."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Color coding
        colors = {
            "user": "#7ef0c1",
            "jarvis": "#00d4ff",
            "system": "#9bb6bd",
            "healer": "#fbbf24",
            "error": "#f87171",
        }
        color = colors.get(speaker, "#e6f7fb")
        
        # Format labels
        labels = {
            "user": "You",
            "jarvis": "Jarvis",
            "system": "SYS",
            "healer": "Healer",
            "error": "ERR",
        }
        label = labels.get(speaker, speaker.upper())
        
        html = f'<span style="color: #1d3c4a;">[{timestamp}]</span> '
        html += f'<span style="color: {color}; font-weight: bold;">{label}:</span> '
        html += f'<span style="color: {color};">{message}</span>'
        
        self.log_text.append(html)
        
        # Auto-scroll to bottom
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def _update_state(self, state: str):
        """Update the visual state."""
        self.current_state = state
        
        # Update voice orb
        if VOICE_ORB_AVAILABLE and hasattr(self, 'voice_orb'):
            self.voice_orb.set_state(state)
        
        # Update label
        if hasattr(self, 'orb_state_label'):
            self.orb_state_label.setText(state.upper())
            
            # Color based on state
            state_colors = {
                "idle": "#9bb6bd",
                "listening": "#7ef0c1",
                "thinking": "#fbbf24",
                "speaking": "#00d4ff",
            }
            color = state_colors.get(state, "#9bb6bd")
            self.orb_state_label.setStyleSheet(f"""
                color: {color};
                font-size: 14px;
                font-weight: bold;
                padding: 5px;
                background-color: #071018;
                border-radius: 6px;
            """)
    
    def _update_status(self, message: str):
        """Update status bar."""
        self.status_label.setText(message)
    
    def _update_time(self):
        """Update time display."""
        now = datetime.now().strftime("%H:%M:%S")
        self.time_label.setText(now)
    
    # ═══════════════════════════════════════════════════════════════
    # EVENT HANDLERS
    # ═══════════════════════════════════════════════════════════════
    
    def _on_interrupt(self):
        """Handle interrupt button."""
        self._append_log("system", "User interrupted JARVIS")
        self.set_state("idle")
        if self.jarvis:
            # Call jarvis interrupt method if available
            if hasattr(self.jarvis, 'interrupt'):
                self.jarvis.interrupt()
    
    def _on_remote_control(self):
        """Handle remote control button."""
        self._append_log("system", "Remote control panel requested")
        # This would open the remote control interface
    
    def _on_search(self):
        """Handle search button."""
        self._append_log("system", "Search mode activated")
    
    def _on_files(self):
        """Handle files button."""
        self._append_log("system", "File browser activated")
    
    def _on_weather(self):
        """Handle weather button."""
        self._append_log("system", "Weather request")
    
    def _on_news(self):
        """Handle news button."""
        self._append_log("system", "News request")
    
    def _on_music(self):
        """Handle music button."""
        self._append_log("system", "Music controls")
    
    def _on_settings(self):
        """Handle settings button."""
        self._append_log("system", "Settings panel")
    
    def _clear_log(self):
        """Clear the conversation log."""
        self.log_text.clear()
        self._append_log("system", "Log cleared")
    
    def _new_session(self):
        """Start a new session."""
        self._clear_log()
        self._append_log("system", "New session started")
        self._append_log("jarvis", "Good day. How may I assist you?")
    
    def _toggle_orb(self):
        """Toggle voice orb visibility."""
        if VOICE_ORB_AVAILABLE and hasattr(self, 'voice_orb'):
            visible = self.voice_orb.isVisible()
            self.voice_orb.setVisible(not visible)
    
    def _view_memory(self):
        """View memory contents."""
        self._append_log("system", "Memory viewer requested")
    
    def _view_logs(self):
        """View detailed logs."""
        self._append_log("system", "Log viewer requested")
    
    def _show_about(self):
        """Show about dialog."""
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.about(
            self,
            "About JARVIS",
            "<h2>Mark XLVIII</h2>"
            "<p>A cross-platform AI voice assistant</p>"
            "<p>Built with PyQt6 and Gemini Live API</p>"
            "<p>By Hasan</p>"
            "<p><a href='https://github.com/Onielq/Mark-XLVII'>GitHub</a></p>"
        )
    
    def closeEvent(self, event):
        """Handle window close."""
        if self.jarvis and hasattr(self.jarvis, 'shutdown'):
            self.jarvis.shutdown()
        event.accept()


# ═══════════════════════════════════════════════════════════════
# STANDALONE TEST
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create UI without jarvis instance for testing
    ui = JarvisUI()
    ui.show()
    
    # Demo: cycle through states
    def demo_states():
        states = ["idle", "listening", "thinking", "speaking"]
        idx = [0]
        
        def next_state():
            state = states[idx[0] % len(states)]
            ui.set_state(state)
            ui.write_log("system", f"State changed to: {state}")
            
            # Simulate audio for speaking/listening
            if state in ("listening", "speaking"):
                import random
                ui.set_audio_bands(
                    random.random(),
                    random.random(),
                    random.random()
                )
            
            idx[0] += 1
        
        timer = QTimer()
        timer.timeout.connect(next_state)
        timer.start(2000)
    
    demo_states()
    
    sys.exit(app.exec())
