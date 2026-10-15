"""
INTEGRATION GUIDE - Adding Voice Orb to Mark XLVIII

This shows how to add the voice orb to your existing PyQt6 UI.
"""

# ═══════════════════════════════════════════════════════════════
# STEP 1: Install Dependencies
# ═══════════════════════════════════════════════════════════════

"""
pip install PyQt6 PyOpenGL numpy
"""

# ═══════════════════════════════════════════════════════════════
# STEP 2: Copy voice_orb.py to your project
# ═══════════════════════════════════════════════════════════════

"""
Copy: public/UPDATE_FILES/voice_orb.py
To:   Mark-XLVII/voice_orb.py
"""

# ═══════════════════════════════════════════════════════════════
# STEP 3: Modify ui.py to include the voice orb
# ═══════════════════════════════════════════════════════════════

"""
In your ui.py file, add this import at the top:

from voice_orb import VoiceOrb

Then in your main window class, add the orb:

class JarvisUI(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Create central widget and layout
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Add voice orb
        self.voice_orb = VoiceOrb(self)
        self.voice_orb.setMinimumSize(300, 300)
        layout.addWidget(self.voice_orb)
        
        # ... rest of your UI code
"""

# ═══════════════════════════════════════════════════════════════
# STEP 4: Connect audio analysis to the orb
# ═══════════════════════════════════════════════════════════════

"""
In your main.py or audio processing code, add:

import numpy as np
from scipy import signal

class AudioAnalyzer:
    def __init__(self, voice_orb):
        self.orb = voice_orb
        self.sample_rate = 44100
        self.fft_size = 2048
    
    def analyze(self, audio_data):
        # Calculate FFT
        fft = np.fft.rfft(audio_data, n=self.fft_size)
        magnitudes = np.abs(fft)
        
        # Split into frequency bands
        freqs = np.fft.rfftfreq(self.fft_size, 1.0 / self.sample_rate)
        
        # Low: 45-250 Hz
        low_mask = (freqs >= 45) & (freqs <= 250)
        low_energy = np.mean(magnitudes[low_mask]) if np.any(low_mask) else 0
        
        # Mid: 250-2400 Hz
        mid_mask = (freqs >= 250) & (freqs <= 2400)
        mid_energy = np.mean(magnitudes[mid_mask]) if np.any(mid_mask) else 0
        
        # High: 2400-12000 Hz
        high_mask = (freqs >= 2400) & (freqs <= 12000)
        high_energy = np.mean(magnitudes[high_mask]) if np.any(high_mask) else 0
        
        # Normalize to 0-1
        max_energy = max(low_energy, mid_energy, high_energy, 1.0)
        low = low_energy / max_energy
        mid = mid_energy / max_energy
        high = high_energy / max_energy
        
        # Beat detection (simple onset)
        onset = 0.0
        if low > 0.7:
            onset = low - 0.7
        
        # Update the orb
        self.orb.set_audio_bands(low, mid, high)
        self.orb.set_onset(onset)

# In your main loop:
audio_analyzer = AudioAnalyzer(self.voice_orb)

# When you receive audio data:
audio_analyzer.analyze(audio_data)
"""

# ═══════════════════════════════════════════════════════════════
# STEP 5: Update orb state based on JARVIS state
# ═══════════════════════════════════════════════════════════════

"""
In your main.py, when JARVIS state changes:

# When listening to user:
self.voice_orb.set_state("listening")

# When thinking/processing:
self.voice_orb.set_state("thinking")

# When speaking response:
self.voice_orb.set_state("speaking")

# When idle:
self.voice_orb.set_state("idle")
"""

# ═══════════════════════════════════════════════════════════════
# COMPLETE EXAMPLE - Minimal Integration
# ═══════════════════════════════════════════════════════════════

"""
# In main.py, add this minimal integration:

from voice_orb import VoiceOrb
import numpy as np

class JarvisLive:
    def __init__(self):
        # ... your existing init code ...
        
        # Add voice orb to UI
        self.voice_orb = VoiceOrb()
        self.ui.layout.addWidget(self.voice_orb)  # Assuming you have a layout
        
        # Audio analyzer
        self.audio_analyzer = self._create_audio_analyzer()
    
    def _create_audio_analyzer(self):
        def analyze(audio_data):
            # Simple FFT analysis
            fft = np.fft.rfft(audio_data, n=2048)
            magnitudes = np.abs(fft)
            
            # Split into bands (simplified)
            low = np.mean(magnitudes[:50]) / 1000
            mid = np.mean(magnitudes[50:500]) / 1000
            high = np.mean(magnitudes[500:]) / 1000
            
            # Normalize
            max_val = max(low, mid, high, 1.0)
            self.voice_orb.set_audio_bands(
                min(1.0, low / max_val),
                min(1.0, mid / max_val),
                min(1.0, high / max_val)
            )
        
        return analyze
    
    def on_user_speaking(self):
        self.voice_orb.set_state("listening")
    
    def on_processing(self):
        self.voice_orb.set_state("thinking")
    
    def on_speaking(self):
        self.voice_orb.set_state("speaking")
    
    def on_idle(self):
        self.voice_orb.set_state("idle")
"""

# ═══════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════

"""
To test the voice orb standalone:

python voice_orb.py

This will open a window with the orb and buttons to change states.
"""

print(__doc__)
