"""
voice_orb.py - PyQt6 Voice Orb Visualization

A WebGL-like particle system for the desktop app.
Reacts to audio input in real-time.

REQUIRES: pip install PyQt6 numpy
"""

import sys
import math
import random
import numpy as np
from PyQt6.QtWidgets import QOpenGLWidget
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen
from OpenGL.GL import *
from OpenGL.GLU import *


class VoiceOrb(QOpenGLWidget):
    """
    Voice-reactive particle orb for PyQt6.
    Similar to the web version but rendered with OpenGL.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 400)
        
        # State: idle, listening, thinking, speaking
        self.state = "idle"
        
        # Particle system
        self.num_particles = 8000
        self.particles = []
        self._init_particles()
        
        # Audio data (will be set externally)
        self.audio_bands = [0.0, 0.0, 0.0]  # low, mid, high
        self.onset = 0.0
        
        # Animation
        self.time = 0.0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_orb)
        self.timer.start(16)  # ~60 FPS
        
        # Colors for each state
        self.state_colors = {
            "idle": (0.62, 0.60, 0.87),      # Lilac
            "listening": (0.16, 0.91, 0.71), # Turquoise
            "thinking": (1.0, 0.57, 0.18),   # Amber
            "speaking": (0.96, 0.27, 0.62),  # Pink
        }
    
    def _init_particles(self):
        """Initialize particle positions on a sphere."""
        self.particles = []
        for i in range(self.num_particles):
            # Fibonacci sphere distribution
            y = 1 - (i / float(self.num_particles - 1)) * 2
            radius = math.sqrt(1 - y * y)
            theta = i * 2.399963  # Golden angle
            
            x = math.cos(theta) * radius
            z = math.sin(theta) * radius
            
            self.particles.append({
                'pos': [x, y, z],
                'seed': random.random(),
                'base_pos': [x, y, z]
            })
    
    def set_state(self, state: str):
        """Set the orb state (idle, listening, thinking, speaking)."""
        if state in self.state_colors:
            self.state = state
            self.update()
    
    def set_audio_bands(self, low: float, mid: float, high: float):
        """Set audio frequency bands (0.0 to 1.0)."""
        self.audio_bands = [
            max(0.0, min(1.0, low)),
            max(0.0, min(1.0, mid)),
            max(0.0, min(1.0, high))
        ]
        self.update()
    
    def set_onset(self, onset: float):
        """Set beat onset detection (0.0 to 1.0)."""
        self.onset = max(0.0, min(1.0, onset))
        self.update()
    
    def update_orb(self):
        """Update animation."""
        self.time += 0.016
        self.update()
    
    def initializeGL(self):
        """Initialize OpenGL."""
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_POINT_SMOOTH)
    
    def resizeGL(self, w, h):
        """Handle resize."""
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
    
    def paintGL(self):
        """Render the orb."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -3.5)
        
        # Get current color based on state
        color = self.state_colors.get(self.state, self.state_colors["idle"])
        
        # Draw particles
        glPointSize(3.0)
        glBegin(GL_POINTS)
        
        low, mid, high = self.audio_bands
        
        for p in self.particles:
            x, y, z = p['base_pos']
            seed = p['seed']
            
            # Apply state-based transformations
            if self.state == "idle":
                # Slow drift
                drift = math.sin(self.time * 0.3 + x * 3) * 0.02
                x += drift
                y += math.cos(self.time * 0.2 + y * 3) * 0.02
                z += math.sin(self.time * 0.25 + z * 3) * 0.02
            
            elif self.state == "listening":
                # Pull inward with audio
                angle = math.acos(max(-1, min(1, z)))
                inward = math.sin(angle * 13 + self.time * 5) * 0.1
                scale = 1.0 - low * 0.15 + mid * inward * 0.3
                x *= scale
                y *= scale
                z *= scale
            
            elif self.state == "thinking":
                # Twist around Y axis
                twist = self.time * 0.5 + y * 1.5
                cos_t = math.cos(twist)
                sin_t = math.sin(twist)
                new_x = x * cos_t + z * sin_t
                new_z = z * cos_t - x * sin_t
                x, z = new_x, new_z
                y *= 0.92  # Flatten slightly
            
            elif self.state == "speaking":
                # Push outward with audio
                angle = math.acos(max(-1, min(1, z)))
                outward = math.sin(angle * 12 - self.time * 6) * 0.15
                scale = 1.0 + low * 0.2 + mid * outward * 0.4
                scale += self.onset * 0.15 * (0.4 + 0.6 * seed)
                x *= scale
                y *= scale
                z *= scale
            
            # Calculate depth for size/opacity
            depth = (z + 1.5) / 3.0
            size = 2.0 + depth * 2.0
            
            # Color variation
            cool = 0.5 + 0.5 * math.sin(y * 2 + x * 1.5)
            r = color[0] * (0.7 + 0.3 * cool)
            g = color[1] * (0.7 + 0.3 * cool)
            b = color[2] * (0.7 + 0.3 * cool)
            
            # Brightness based on audio
            brightness = 0.5 + 0.5 * (low + mid + high) / 3.0
            r *= brightness
            g *= brightness
            b *= brightness
            
            glColor4f(r, g, b, 0.6 + depth * 0.4)
            glVertex3f(x, y, z)
        
        glEnd()
        
        # Draw glow in center
        self._draw_glow(color)
    
    def _draw_glow(self, color):
        """Draw central glow effect."""
        # Simple glow using larger transparent points
        glPointSize(20.0)
        glBegin(GL_POINTS)
        glColor4f(color[0], color[1], color[2], 0.1)
        glVertex3f(0, 0, 0)
        glEnd()


# ═══════════════════════════════════════════════════════════════
# Integration Example
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QLabel
    from PyQt6.QtCore import Qt
    
    class TestWindow(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Voice Orb Test")
            self.resize(500, 600)
            
            layout = QVBoxLayout(self)
            
            # Voice orb
            self.orb = VoiceOrb(self)
            layout.addWidget(self.orb)
            
            # State buttons
            btn_layout = QVBoxLayout()
            for state in ["idle", "listening", "thinking", "speaking"]:
                btn = QPushButton(state.capitalize())
                btn.clicked.connect(lambda checked, s=state: self.orb.set_state(s))
                btn_layout.addWidget(btn)
            layout.addLayout(btn_layout)
            
            # Info label
            self.label = QLabel("Click buttons to change state")
            layout.addWidget(self.label)
    
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())
