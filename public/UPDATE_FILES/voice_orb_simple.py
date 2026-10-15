"""
voice_orb_simple.py - Simple Voice Orb for PyQt6

EASY VERSION - Just copy this file and add 3 lines to your code.

INSTALL: pip install PyQt6 PyOpenGL numpy
"""

from PyQt6.QtWidgets import QOpenGLWidget
from PyQt6.QtCore import QTimer
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random


class VoiceOrb(QOpenGLWidget):
    """Simple voice-reactive orb for PyQt6."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 300)
        self.state = "idle"
        self.audio_bands = [0.0, 0.0, 0.0]
        self.time = 0.0
        
        # Create particles
        self.particles = []
        for i in range(5000):
            y = 1 - (i / 4999) * 2
            radius = math.sqrt(1 - y * y)
            theta = i * 2.4
            x = math.cos(theta) * radius
            z = math.sin(theta) * radius
            self.particles.append([x, y, z])
        
        # Animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update)
        self.timer.start(16)
        
        # Colors
        self.colors = {
            "idle": (0.62, 0.60, 0.87),
            "listening": (0.16, 0.91, 0.71),
            "thinking": (1.0, 0.57, 0.18),
            "speaking": (0.96, 0.27, 0.62),
        }
    
    def set_state(self, state):
        """Set state: idle, listening, thinking, speaking"""
        if state in self.colors:
            self.state = state
    
    def set_audio(self, low, mid, high):
        """Set audio levels (0.0 to 1.0)"""
        self.audio_bands = [
            max(0, min(1, low)),
            max(0, min(1, mid)),
            max(0, min(1, high))
        ]
    
    def _update(self):
        self.time += 0.016
        self.update()
    
    def initializeGL(self):
        glClearColor(0, 0, 0, 0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)
        glEnable(GL_POINT_SMOOTH)
    
    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w/h, 0.1, 100)
        glMatrixMode(GL_MODELVIEW)
    
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0, 0, -3.5)
        
        color = self.colors[self.state]
        low, mid, high = self.audio_bands
        
        glPointSize(2.5)
        glBegin(GL_POINTS)
        
        for x, y, z in self.particles:
            # Apply transformations based on state
            if self.state == "idle":
                x += math.sin(self.time * 0.3 + x * 3) * 0.02
                y += math.cos(self.time * 0.2 + y * 3) * 0.02
            
            elif self.state == "listening":
                scale = 1.0 - low * 0.15 + mid * 0.1
                x *= scale
                y *= scale
                z *= scale
            
            elif self.state == "thinking":
                twist = self.time * 0.5 + y * 1.5
                cos_t, sin_t = math.cos(twist), math.sin(twist)
                x, z = x * cos_t + z * sin_t, z * cos_t - x * sin_t
                y *= 0.92
            
            elif self.state == "speaking":
                scale = 1.0 + low * 0.2 + mid * 0.15
                x *= scale
                y *= scale
                z *= scale
            
            # Color
            depth = (z + 1.5) / 3
            brightness = 0.5 + 0.5 * (low + mid + high) / 3
            
            glColor4f(
                color[0] * brightness,
                color[1] * brightness,
                color[2] * brightness,
                0.5 + depth * 0.5
            )
            glVertex3f(x, y, z)
        
        glEnd()


# ═══════════════════════════════════════════════════════════════
# HOW TO USE (3 STEPS)
# ═══════════════════════════════════════════════════════════════

"""
STEP 1: Install dependencies
    pip install PyQt6 PyOpenGL numpy

STEP 2: Copy this file to your Mark-XLVII folder
    Copy: voice_orb_simple.py
    To:   Mark-XLVII/voice_orb_simple.py

STEP 3: Add to your ui.py (3 lines)
    
    # At the top with other imports:
    from voice_orb_simple import VoiceOrb
    
    # In your main window __init__:
    self.voice_orb = VoiceOrb(self)
    self.layout.addWidget(self.voice_orb)  # or however you add widgets
    
    # When state changes:
    self.voice_orb.set_state("listening")  # or "thinking", "speaking", "idle"
    
    # When you have audio data:
    self.voice_orb.set_audio(low, mid, high)  # values 0.0 to 1.0

THAT'S IT! The orb will now show in your PyQt6 app.
"""


# ═══════════════════════════════════════════════════════════════
# TEST IT
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton
    
    class TestWindow(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Voice Orb Test")
            self.resize(400, 500)
            
            layout = QVBoxLayout(self)
            
            # Add orb
            self.orb = VoiceOrb(self)
            layout.addWidget(self.orb)
            
            # Add buttons
            for state in ["idle", "listening", "thinking", "speaking"]:
                btn = QPushButton(state.capitalize())
                btn.clicked.connect(lambda checked, s=state: self.orb.set_state(s))
                layout.addWidget(btn)
    
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())
