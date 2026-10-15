# Voice Orb Integration - Mark XLVIII

## ✅ Successfully Installed

The **Voice Orb** component from [Ship Notes](https://aqualang89.github.io/shipnotes-components/components/voice-orb/demo.html) has been successfully integrated into the Mark XLVIII website.

---

## 🎨 What is the Voice Orb?

A stunning WebGL-based particle visualization that reacts to audio input. It features:

- **12,000 particles** rendered in real-time using WebGL shaders
- **4 distinct states**: idle, listening, thinking, speaking
- **Audio-reactive**: Responds to microphone input or audio playback
- **Three frequency bands**: Bass (45-250Hz), Mid (250-2.4kHz), High (2.4-12kHz)
- **Smooth transitions**: 700ms blend between states
- **Zero dependencies**: Pure WebGL, no external libraries
- **Performance optimized**: 60fps on modern hardware

---

## 📍 Where It's Used

### 1. Hero Section (Main Landing)
- **Location**: Right side of the hero section
- **Size**: 320x320px
- **Features**:
  - Interactive microphone button
  - State toggle buttons (idle, listening, thinking, speaking)
  - Real-time audio visualization when you talk

### 2. Dashboard Section
- **Location**: Main conversation panel
- **Size**: 180x180px
- **Features**:
  - Automatically changes state based on conversation
  - LISTENING state when waiting for input
  - THINKING state when processing
  - SPEAKING state when responding

---

## 🎮 How to Use

### Talk to JARVIS (Hero Section)
1. Click the **"Talk to JARVIS"** button
2. Allow microphone access when prompted
3. Speak - the orb will react to your voice in real-time!
4. Click **"Stop Listening"** to disconnect

### Manual State Control
Use the state buttons to manually switch between:
- **Idle**: Slow lilac sphere (default)
- **Listening**: Turquoise waves pulling inward
- **Thinking**: Amber twisted belts
- **Speaking**: Pink/violet waves pushing outward

---

## 🔧 Technical Details

### File Structure
```
public/
  └── voice-orb.js          # Web component (15KB)

index.html
  └── <script src="/voice-orb.js" defer></script>

src/components/
  ├── Hero.tsx              # Main voice orb with mic controls
  └── Dashboard.tsx         # Dashboard voice orb
```

### Component API
```typescript
<voice-orb 
  state="idle"              // 'idle' | 'listening' | 'thinking' | 'speaking'
  particles={12000}         // Optional: 200-20000 (auto-adjusts for mobile)
  recording={false}         // Optional: Stops animation loop for screenshots
/>

// Connect to audio
const orb = document.querySelector('voice-orb');
await orb.connect(mediaStream);  // or HTMLMediaElement or AudioNode
orb.disconnect();
```

### Audio Analysis
- **FFT Size**: 2048
- **Frequency Bands**:
  - Low: 45-250 Hz (bass pressure, broad deformation)
  - Mid: 250-2,400 Hz (traveling folds)
  - High: 2,400-12,000 Hz (fine noise, edge sparks)
- **Attack/Release**: Different for each band (6-28ms attack, 85-200ms release)
- **Kick Detection**: Fast 60ms baseline cancels rolling bass, catches kicks

---

## 🎨 Visual States

### Idle
- **Color**: Lilac/purple
- **Movement**: Slow drift, gentle breathing
- **Particles**: 12,000 points in spherical formation

### Listening
- **Color**: Turquoise/cyan
- **Movement**: Waves pull inward toward center
- **Audio Response**: Bass creates broad deformation, mids create traveling folds

### Thinking
- **Color**: Amber/orange
- **Movement**: Three narrow belts twist around sphere
- **Special**: Bright heads move along the belts

### Speaking
- **Color**: Pink/violet
- **Movement**: Waves push outward from center
- **Audio Response**: Bass creates outward pressure, highs create edge sparks

---

## 🚀 Performance

### Benchmarks (from original component)
- **12,000 particles at 720x720**: 60fps (software renderer)
- **Automatic quality scaling**: Drops to 800 particles on slow frames
- **Mobile optimization**: 6,000 particles on touch devices
- **Canvas 2D fallback**: 1,000 particles if WebGL unavailable

### Browser Support
- ✅ Chrome/Edge (WebGL)
- ✅ Firefox (WebGL)
- ✅ Safari (WebGL)
- ✅ Mobile browsers (auto-scaled)
- ✅ Reduced motion support (static display)

---

## 🔒 Privacy & Security

- **No network requests**: All processing is local
- **No data collection**: Audio stays in your browser
- **No AI services**: Pure visualization
- **Microphone permission**: Only requested when you click "Talk to JARVIS"
- **No recording**: Audio is analyzed in real-time, never stored

---

## 🎯 Integration with Mark XLVIII

The voice orb serves as the visual representation of JARVIS's state:

1. **Idle**: JARVIS is waiting for commands
2. **Listening**: JARVIS is hearing your voice
3. **Thinking**: JARVIS is processing your request
4. **Speaking**: JARVIS is responding

In the actual Python application, the orb would be connected to:
- Gemini Live API audio stream
- Microphone input
- System state changes

---

## 📚 Resources

- **Original Demo**: https://aqualang89.github.io/shipnotes-components/components/voice-orb/demo.html
- **Source Code**: https://github.com/aqualang89/shipnotes-components/tree/main/components/voice-orb
- **License**: MIT (check repository for details)

---

## 🎉 What's Next?

The voice orb is now fully integrated and functional. To experience it:

1. **Visit the website** and scroll to the Hero section
2. **Click "Talk to JARVIS"** and allow microphone access
3. **Speak** and watch the orb react to your voice!
4. **Try the state buttons** to see different visual modes
5. **Scroll down** to the Dashboard section to see it in action there too

---

**Status**: ✅ Production Ready  
**Installed**: 2026-01-XX  
**Version**: Latest (Sep 26, 2026 commit)
