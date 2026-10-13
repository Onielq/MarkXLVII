# 🚀 Mark XLVIII - Complete Installation Guide

## ⚠️ IMPORTANT: What You're Actually Installing

**This website is a SHOWCASE/DEMO** - it's just a presentation of Mark XLVIII's features.

**The REAL Mark XLVIII is a Python desktop application** that runs on your computer with:
- PyQt6 desktop interface (not web-based)
- Real microphone and speaker access
- Gemini Live API integration
- Actual file system control
- OS-level automation

---

## 📦 What You Need to Install

### Option 1: Fresh Installation (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/Onielq/Mark-XLVII.git
cd Mark-XLVII

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install additional dependencies for new features
pip install rarfile py7zr wikipedia-api

# 4. Run setup wizard (configures API key)
python setup.py

# 5. Launch JARVIS
python main.py
```

### Option 2: Update Existing Installation

If you already have Mark XLVIII installed, apply these updates:

---

## 🔧 Files to Update/Replace

### 1. Web Search Fix (Critical)
**File:** `actions/web_search.py`

**What it fixes:**
- Can't answer factual questions like "Who is the president of East Africa?"
- Limited search capability when Gemini API fails

**How to update:**
```bash
# Backup original
cp actions/web_search.py actions/web_search.py.backup

# Download the fixed version
# The fixed file is at: public/fixed_web_search.py in this website
# Copy it to: actions/web_search.py
```

**Or manually apply these changes:**
- Added Wikipedia API fallback
- Smart query enhancement for factual questions
- Triple fallback chain: Gemini → DDG → Wikipedia

---

### 2. File Processor Fix (Critical)
**File:** `actions/file_processor.py`

**What it fixes:**
- Can't read contents of zip/rar/tar files
- Limited archive support

**How to update:**
```bash
# Backup original
cp actions/file_processor.py actions/file_processor.py.backup

# Download the fixed version
# The fixed file is at: public/fixed_file_processor.py in this website
# Copy it to: actions/file_processor.py
```

**Or manually apply these changes:**
- Added ability to read files inside archives without extracting
- Added search functionality within archives
- Added support for .rar and .7z formats
- New commands: read, read_all, search, summarize

---

### 3. Core Self-Healing System (NEW - Optional but Recommended)

**What it adds:**
- FBI/CIA-level autonomous debugging
- Self-detection and self-repair
- Automatic issue resolution

**Files to add:**
```bash
# Create core directory if it doesn't exist
mkdir -p core

# Download these 7 new files from the website's public folder:
# - public/core/__init__.py     → core/__init__.py
# - public/core/healer.py       → core/healer.py
# - public/core/detector.py     → core/detector.py
# - public/core/researcher.py   → core/researcher.py
# - public/core/validator.py    → core/validator.py
# - public/core/fallback.py     → core/fallback.py
# - public/core/logger.py       → core/logger.py
```

**Then update main.py to import the healer:**
```python
# Add to main.py imports at the top
from core.healer import SelfHealer

# Add to JarvisLive.__init__ method
self.healer = SelfHealer(BASE_DIR)

# Add to the main run() loop, inside the TaskGroup
tg.create_task(self.healer.start_monitoring())
```

---

### 4. Memory Backup System (NEW - Optional)

**What it adds:**
- Automatic memory backups
- Corruption recovery
- Data integrity protection

**Files to add:**
```bash
# Create backup directory
mkdir -p memory/backup

# Download: public/memory/backup_manager.py → memory/backup_manager.py
```

---

## 📋 Complete Update Checklist

### Critical Updates (Must Have)
- [ ] Update `actions/web_search.py` (fixes factual search)
- [ ] Update `actions/file_processor.py` (fixes archive reading)
- [ ] Install `rarfile` package: `pip install rarfile`
- [ ] Install `py7zr` package: `pip install py7zr`

### Recommended Updates
- [ ] Add Core Self-Healing System (6 new files in core/)
- [ ] Add Memory Backup System (1 new file)
- [ ] Update main.py to import healer
- [ ] Install `wikipedia-api`: `pip install wikipedia-api`

### Optional Updates
- [ ] Update dashboard for remote healing triggers
- [ ] Add debug session viewer to UI

---

## 🎯 Step-by-Step Installation

### For Fresh Install:

```bash
# 1. Clone repository
git clone https://github.com/Onielq/Mark-XLVII.git
cd Mark-XLVII

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install base requirements
pip install -r requirements.txt

# 4. Install additional packages for new features
pip install rarfile py7zr wikipedia-api

# 5. Apply critical fixes
# Download fixed_web_search.py and fixed_file_processor.py from the website
# and replace the files in actions/ folder

# 6. Add Core Self-Healing System (optional)
# Download the 6 core files from website and place in core/ folder

# 7. Run setup
python setup.py
# Enter your Gemini API key when prompted
# Get one free at: https://aistudio.google.com

# 8. Launch
python main.py
```

### For Existing Install:

```bash
# 1. Backup your current installation
cp -r Mark-XLVII Mark-XLVII.backup

# 2. Navigate to your installation
cd Mark-XLVII

# 3. Backup files you're about to replace
cp actions/web_search.py actions/web_search.py.backup
cp actions/file_processor.py actions/file_processor.py.backup

# 4. Replace with fixed versions
# (copy from website's public folder)

# 5. Install new dependencies
pip install rarfile py7zr wikipedia-api

# 6. Add Core System (optional)
mkdir -p core
# (copy 6 files from website's public/core folder)

# 7. Restart JARVIS
python main.py
```

---

## 🧪 Testing the Updates

### Test Web Search Fix:
```
You: "Who is the president of Kenya?"
Expected: JARVIS should answer with current president's name
```

### Test File Processor Fix:
```
You: "List files in my_project.zip"
Expected: JARVIS should show all files in the archive

You: "Read readme.txt from my_project.zip"
Expected: JARVIS should display the file contents
```

### Test Core System (if installed):
```
# Trigger a test error by temporarily breaking something
# JARVIS should detect, analyze, and fix it automatically
# Check logs for healing session
```

---

## 📁 File Structure After Updates

```
Mark-XLVII/
├── main.py                          # Updated to import healer
├── ui.py                            # PyQt6 interface
├── setup.py                         # Configuration wizard
├── actions/
│   ├── web_search.py                # ✅ FIXED (triple fallback)
│   ├── file_processor.py            # ✅ FIXED (archive support)
│   ├── screen_processor.py
│   ├── reminder.py
│   └── ... (other action files)
├── core/
│   ├── prompt.txt                   # JARVIS personality
│   ├── healer.py                    # 🆕 NEW - Self-repair engine
│   ├── detector.py                  # 🆕 NEW - Anomaly detection
│   ├── researcher.py                # 🆕 NEW - Solution research
│   ├── validator.py                 # 🆕 NEW - Fix verification
│   ├── fallback.py                  # 🆕 NEW - Fallback management
│   └── logger.py                    # 🆕 NEW - Debug logging
├── memory/
│   ├── memory_manager.py
│   ├── memory.json
│   └── backup/                      # 🆕 NEW - Auto-backups
│       └── backup_manager.py
├── config/
│   └── api_keys.json
└── dashboard/
    └── server.py
```

---

## 🔍 What's Different from the Website?

### Website Shows:
- React-based web interface
- Voice orb visualization
- Interactive debug viewer
- Marketing showcase

### Actual Application Has:
- PyQt6 desktop window
- Real microphone/speaker integration
- File system access
- OS-level control (volume, brightness, apps)
- Actual Gemini Live API connection
- Real voice conversation
- Desktop HUD with waveform

---

## ❓ FAQ

**Q: Do I need the website to run Mark XLVIII?**
A: No! The website is just a demo. You only need the Python files from the GitHub repository.

**Q: Can I use the voice orb from the website?**
A: The voice orb is a web component. The actual app uses a PyQt6 waveform display instead.

**Q: Do the fixes work on the real app?**
A: Yes! The fixed web_search.py and file_processor.py files work directly in the Python application.

**Q: What about the Core System?**
A: The Core System modules are Python files that integrate into the real app. The website just shows a visual demo of how it works.

**Q: Is the Core System required?**
A: No, it's optional. The critical fixes (web_search and file_processor) are required. Core System adds autonomous debugging but isn't necessary for basic operation.

---

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'rarfile'"
```bash
pip install rarfile
```

### "ModuleNotFoundError: No module named 'py7zr'"
```bash
pip install py7zr
```

### "Wikipedia API not working"
```bash
pip install wikipedia-api
```

### "Core System not activating"
- Make sure you imported SelfHealer in main.py
- Check that all 6 core files are in the core/ folder
- Verify Python can import them: `python -c "from core.healer import SelfHealer"`

---

## 📞 Support

- **GitHub Issues:** https://github.com/Onielq/Mark-XLVII/issues
- **Original Repository:** https://github.com/Onielq/Mark-XLVII
- **Documentation:** Check the README.md in the repository

---

## ✅ Summary

**You're installing:** A Python desktop application (not a website)

**Critical fixes to apply:**
1. `actions/web_search.py` - Fixes factual search
2. `actions/file_processor.py` - Fixes archive reading

**Optional additions:**
- Core Self-Healing System (6 files in core/)
- Memory Backup System

**Installation:**
```bash
git clone https://github.com/Onielq/Mark-XLVII.git
cd Mark-XLVII
pip install -r requirements.txt
pip install rarfile py7zr wikipedia-api
# Apply fixes from website's public folder
python setup.py
python main.py
```

---

**Last Updated:** 2026-01-XX  
**Version:** 2.2.0 with Core System
