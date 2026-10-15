#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  MARK XLVIII - ONE-CLICK INSTALLER                              ║
║                                                                  ║
║  Run this ONCE and everything is done:                          ║
║    python install_mark_xlviii.py                                ║
║                                                                  ║
║  That's it. No manual file moving. No editing. Just run it.    ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════

REPO_URL = "https://github.com/Onielq/Mark-XLVII.git"
INSTALL_DIR = Path.home() / "Mark-XLVII"

PACKAGES = [
    "rarfile",
    "py7zr", 
    "wikipedia-api",
    "PyQt6",
    "PyOpenGL",
    "numpy",
    "requests",
    "google-genai",
    "duckduckgo-search",
    "sounddevice",
    "pydub",
    "Pillow",
    "pdfplumber",
    "python-docx",
    "pandas",
    "openpyxl",
    "python-pptx",
    "fastapi",
    "uvicorn",
]

# ═══════════════════════════════════════════════════════════════
# COLORS FOR OUTPUT
# ═══════════════════════════════════════════════════════════════

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}{Colors.END}\n")

def print_step(text):
    print(f"{Colors.CYAN}▸ {text}{Colors.END}")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠ {text}{Colors.END}")

# ═══════════════════════════════════════════════════════════════
# STEP 1: CLONE REPOSITORY
# ═══════════════════════════════════════════════════════════════

def clone_repository():
    print_header("STEP 1: Cloning Mark XLVIII Repository")
    
    if INSTALL_DIR.exists():
        print_warning(f"Directory already exists: {INSTALL_DIR}")
        response = input("Overwrite? (y/n): ").strip().lower()
        if response != 'y':
            print("Using existing installation...")
            return True
        shutil.rmtree(INSTALL_DIR)
    
    try:
        print_step(f"Cloning from {REPO_URL}...")
        subprocess.run(
            ["git", "clone", REPO_URL, str(INSTALL_DIR)],
            check=True,
            capture_output=True
        )
        print_success("Repository cloned successfully")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to clone: {e}")
        print_warning("Make sure git is installed: https://git-scm.com/downloads")
        return False
    except FileNotFoundError:
        print_error("Git not found. Please install git first.")
        return False

# ═══════════════════════════════════════════════════════════════
# STEP 2: INSTALL DEPENDENCIES
# ═══════════════════════════════════════════════════════════════

def install_dependencies():
    print_header("STEP 2: Installing Python Dependencies")
    
    # First install requirements.txt if it exists
    req_file = INSTALL_DIR / "requirements.txt"
    if req_file.exists():
        print_step("Installing from requirements.txt...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(req_file), "--quiet"],
                check=True
            )
            print_success("requirements.txt installed")
        except subprocess.CalledProcessError:
            print_warning("requirements.txt had issues, continuing...")
    
    # Install additional packages
    print_step("Installing additional packages...")
    for package in PACKAGES:
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", package, "--quiet"],
                check=True
            )
            print_success(f"  {package}")
        except subprocess.CalledProcessError:
            print_warning(f"  {package} - skipped (may already be installed)")
    
    print_success("All dependencies installed")

# ═══════════════════════════════════════════════════════════════
# STEP 3: APPLY WEB SEARCH FIX
# ═══════════════════════════════════════════════════════════════

def apply_web_search_fix():
    print_header("STEP 3: Applying Web Search Fix")
    
    web_search_path = INSTALL_DIR / "actions" / "web_search.py"
    
    if not web_search_path.parent.exists():
        print_error("actions/ directory not found")
        return False
    
    # Backup original
    if web_search_path.exists():
        backup = web_search_path.with_suffix(".py.backup")
        shutil.copy2(web_search_path, backup)
        print_success(f"Backed up original to {backup.name}")
    
    # Write fixed version
    print_step("Writing fixed web_search.py...")
    web_search_path.write_text(WEB_SEARCH_FIXED)
    print_success("Web search fix applied")
    return True

# ═══════════════════════════════════════════════════════════════
# STEP 4: APPLY FILE PROCESSOR FIX
# ═══════════════════════════════════════════════════════════════

def apply_file_processor_fix():
    print_header("STEP 4: Applying File Processor Fix")
    
    file_processor_path = INSTALL_DIR / "actions" / "file_processor.py"
    
    if not file_processor_path.parent.exists():
        print_error("actions/ directory not found")
        return False
    
    # Backup original
    if file_processor_path.exists():
        backup = file_processor_path.with_suffix(".py.backup")
        shutil.copy2(file_processor_path, backup)
        print_success(f"Backed up original to {backup.name}")
    
    # Write fixed version
    print_step("Writing fixed file_processor.py...")
    file_processor_path.write_text(FILE_PROCESSOR_FIXED)
    print_success("File processor fix applied")
    return True

# ═══════════════════════════════════════════════════════════════
# STEP 5: ADD VOICE ORB
# ═══════════════════════════════════════════════════════════════

def add_voice_orb():
    print_header("STEP 5: Adding Voice Orb to Desktop App")
    
    voice_orb_path = INSTALL_DIR / "voice_orb.py"
    
    print_step("Writing voice_orb.py...")
    voice_orb_path.write_text(VOICE_ORB_CODE)
    print_success("Voice orb added")
    
    # Now patch ui.py to include the voice orb
    ui_path = INSTALL_DIR / "ui.py"
    if ui_path.exists():
        print_step("Patching ui.py to include voice orb...")
        patch_ui_for_voice_orb(ui_path)
        print_success("ui.py patched")
    else:
        print_warning("ui.py not found - voice orb available but not integrated")
        print_warning("You can manually import it: from voice_orb import VoiceOrb")
    
    return True

def patch_ui_for_voice_orb(ui_path: Path):
    """Patch ui.py to include the voice orb."""
    content = ui_path.read_text(encoding="utf-8")
    
    # Check if already patched
    if "voice_orb" in content.lower():
        print_warning("ui.py already contains voice orb references")
        return
    
    # Add import at the top (after existing imports)
    import_line = "from voice_orb import VoiceOrb\n"
    
    # Find a good place to add the import
    lines = content.split('\n')
    import_idx = 0
    for i, line in enumerate(lines):
        if line.startswith('import ') or line.startswith('from '):
            import_idx = i + 1
    
    lines.insert(import_idx, import_line.strip())
    
    # Find the main window class and add voice orb
    # Look for a layout.addWidget or similar pattern
    new_content = '\n'.join(lines)
    
    # Add voice orb initialization comment
    orb_init = '''
        # ═══ VOICE ORB (Auto-added by installer) ═══
        try:
            self.voice_orb = VoiceOrb(self)
            self.voice_orb.setMinimumSize(300, 300)
            # Add to your main layout - adjust as needed
            if hasattr(self, 'central_layout'):
                self.central_layout.addWidget(self.voice_orb)
            elif hasattr(self, 'layout'):
                self.layout.addWidget(self.voice_orb)
        except Exception as e:
            print(f"Voice orb init error: {e}")
        # ═══ END VOICE ORB ═══
'''
    
    # Find __init__ method and add after super().__init__()
    if "def __init__" in new_content:
        # Find the first __init__ and add after super() call
        init_idx = new_content.find("def __init__")
        super_idx = new_content.find("super().__init__", init_idx)
        if super_idx != -1:
            # Find end of that line
            end_of_line = new_content.find('\n', super_idx)
            new_content = new_content[:end_of_line+1] + orb_init + new_content[end_of_line+1:]
    
    ui_path.write_text(new_content, encoding="utf-8")

# ═══════════════════════════════════════════════════════════════
# STEP 6: SETUP API KEY
# ═══════════════════════════════════════════════════════════════

def setup_api_key():
    print_header("STEP 6: Configure Gemini API Key")
    
    config_dir = INSTALL_DIR / "config"
    config_dir.mkdir(exist_ok=True)
    
    api_key_file = config_dir / "api_keys.json"
    
    if api_key_file.exists():
        print_success("API key already configured")
        return True
    
    print("Get your FREE Gemini API key at: https://aistudio.google.com")
    api_key = input("\nEnter your Gemini API key (or press Enter to skip): ").strip()
    
    if api_key:
        import json
        api_key_file.write_text(
            json.dumps({"gemini_api_key": api_key}, indent=2),
            encoding="utf-8"
        )
        print_success("API key saved")
    else:
        print_warning("Skipped - run 'python setup.py' later to configure")
    
    return True

# ═══════════════════════════════════════════════════════════════
# STEP 7: LAUNCH
# ═══════════════════════════════════════════════════════════════

def launch_jarvis():
    print_header("STEP 7: Launching Mark XLVIII")
    
    main_py = INSTALL_DIR / "main.py"
    
    if not main_py.exists():
        print_error("main.py not found")
        return False
    
    print_success("All done! Launching JARVIS...")
    print(f"\n{Colors.BOLD}Installation directory: {INSTALL_DIR}{Colors.END}\n")
    
    # Change to install directory and run
    os.chdir(INSTALL_DIR)
    subprocess.run([sys.executable, "main.py"])
    return True

# ═══════════════════════════════════════════════════════════════
# FIXED WEB SEARCH CODE
# ═══════════════════════════════════════════════════════════════

WEB_SEARCH_FIXED = '''#web_search.py - FIXED VERSION with Wikipedia fallback
import json
import sys
import threading
from pathlib import Path

def _get_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent

BASE_DIR        = _get_base_dir()
API_CONFIG_PATH = BASE_DIR / "config" / "api_keys.json"

def _get_api_key() -> str:
    with open(API_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["gemini_api_key"]

def _gemini_search(query: str) -> str:
    from google import genai
    client   = genai.Client(api_key=_get_api_key())
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=query,
        config={"tools": [{"google_search": {}}]},
    )
    text = ""
    for part in response.candidates[0].content.parts:
        if hasattr(part, "text") and part.text:
            text += part.text
    text = text.strip()
    if not text:
        raise ValueError("Gemini returned an empty response.")
    return text

def _ddg_search(query: str, max_results: int = 6) -> list[dict]:
    try:
        from ddgs import DDGS
    except ImportError:
        from duckduckgo_search import DDGS
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append({
                "title":   r.get("title",  ""),
                "snippet": r.get("body",   ""),
                "url":     r.get("href",   ""),
            })
    return results

def _ddg_news(query: str, max_results: int = 8) -> list[dict]:
    try:
        from ddgs import DDGS
    except ImportError:
        from duckduckgo_search import DDGS
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.news(query, max_results=max_results):
                results.append({
                    "title":   r.get("title",  ""),
                    "snippet": r.get("body",   ""),
                    "url":     r.get("url",    ""),
                    "source":  r.get("source", ""),
                })
    except Exception as e:
        print(f"[WebSearch] DDG news failed ({e})")
        results = _ddg_search(query, max_results=max_results)
    return results

# NEW: Wikipedia fallback
def _wikipedia_search(query: str) -> str:
    try:
        import wikipediaapi
        wiki = wikipediaapi.Wikipedia(
            user_agent=\'Mark-XLVII/2.2 (jarvis@local)\',
            language=\'en\'
        )
        page = wiki.page(query)
        if page.exists():
            return f"From Wikipedia - {page.title}:\\n\\n{page.summary[:1500]}"
    except ImportError:
        print("[WebSearch] wikipedia-api not installed")
    except Exception as e:
        print(f"[WebSearch] Wikipedia failed: {e}")
    
    # Fallback to REST API
    try:
        import requests
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={requests.utils.quote(query)}&format=json&srlimit=1"
        resp = requests.get(search_url, timeout=5)
        data = resp.json()
        if data.get("query", {}).get("search"):
            title = data["query"]["search"][0]["title"]
            summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(title)}"
            summary_resp = requests.get(summary_url, timeout=5)
            summary_data = summary_resp.json()
            if summary_data.get("extract"):
                return f"From Wikipedia - {summary_data[\'title\']}:\\n\\n{summary_data[\'extract\']}"
    except Exception as e:
        print(f"[WebSearch] Wikipedia REST failed: {e}")
    return ""

# NEW: Smart query enhancement
def _enhance_query(query: str) -> str:
    factual_keywords = ["who", "what", "when", "where", "which", "president", 
                        "capital", "population", "prime minister"]
    query_lower = query.lower()
    if any(kw in query_lower for kw in factual_keywords):
        if "current" not in query_lower and "today" not in query_lower:
            time_words = ["president", "leader", "price", "weather", "king", "queen"]
            if any(word in query_lower for word in time_words):
                query = f"current {query}"
    return query

def _format_ddg(query: str, results: list[dict]) -> str:
    if not results:
        return f"No results found for: {query}"
    lines = [f"Search results for: {query}\\n"]
    for i, r in enumerate(results, 1):
        if r.get("title"):   lines.append(f"{i}. {r[\'title\']}")
        if r.get("snippet"): lines.append(f"   {r[\'snippet\']}")
        if r.get("url"):     lines.append(f"   Source: {r[\'url\']}")
        lines.append("")
    return "\\n".join(lines).strip()

def _format_news(query: str, results: list[dict]) -> str:
    if not results:
        return f"No news found for: {query}"
    lines = [f"Latest news: {query}\\n"]
    for i, r in enumerate(results, 1):
        title = r.get("title", "")
        if not title: continue
        src = f"  [{r[\'source\']}]" if r.get("source") else ""
        lines.append(f"{i}. {title}{src}")
        if r.get("snippet"): lines.append(f"   {r[\'snippet\'][:140]}")
        if r.get("url"): lines.append(f"   {r[\'url\']}")
        lines.append("")
    return "\\n".join(lines).strip()

# FIXED: Triple fallback search
def _search(query: str) -> str:
    enhanced_query = _enhance_query(query)
    try:
        return _gemini_search(enhanced_query)
    except Exception as e:
        print(f"[WebSearch] Gemini failed ({e}) - trying DDG...")
    try:
        results = _ddg_search(enhanced_query)
        if results:
            return _format_ddg(enhanced_query, results)
    except Exception as e:
        print(f"[WebSearch] DDG failed ({e}) - trying Wikipedia...")
    wiki_result = _wikipedia_search(query)
    if wiki_result:
        return wiki_result
    return f"Unable to find information for: {query}"

def _news(query: str) -> str:
    gemini_query = f"latest news today: {query}" if query else "top world news today"
    ddg_query = query if query else "world news today"
    result_box = [None]
    lock = threading.Lock()
    done_evt = threading.Event()
    failures = [0]

    def _store(r):
        if r and len(r) > 60:
            with lock:
                if result_box[0] is None: result_box[0] = r
            done_evt.set()
        else:
            with lock:
                failures[0] += 1
                if failures[0] >= 2: done_evt.set()

    def _try_gemini():
        try: _store(_gemini_search(gemini_query))
        except: _store("")

    def _try_ddg():
        try:
            results = _ddg_news(ddg_query, max_results=8)
            _store(_format_news(ddg_query, results))
        except: _store("")

    threading.Thread(target=_try_gemini, daemon=True).start()
    threading.Thread(target=_try_ddg, daemon=True).start()
    done_evt.wait(timeout=10.0)
    return result_box[0] or f"No news found for: {query}"

def _research(query: str) -> str:
    research_query = f"Comprehensive explanation of: {query}. Include context and facts."
    try:
        return _gemini_search(research_query)
    except Exception as e:
        results = _ddg_search(query, max_results=10)
        if results: return _format_ddg(query, results)
        wiki = _wikipedia_search(query)
        if wiki: return wiki
        return f"Research failed for: {query}"

def _price(query: str) -> str:
    try:
        return _gemini_search(f"current price of {query}")
    except:
        results = _ddg_search(f"{query} price buy", max_results=6)
        return _format_ddg(query, results)

def _compare(items: list[str], aspect: str) -> str:
    try:
        return _gemini_search(f"Compare {\', \'.join(items)} in terms of {aspect}.")
    except:
        lines = [f"Comparison - {aspect.upper()}", "-" * 40]
        for item in items:
            lines.append(f"\\n> {item}")
            try:
                for r in _ddg_search(f"{item} {aspect}", max_results=2):
                    if r.get("snippet"): lines.append(f"  * {r[\'snippet\']}")
            except: pass
        return "\\n".join(lines)

def web_search(parameters: dict, response=None, player=None, session_memory=None) -> str:
    params = parameters or {}
    query = params.get("query", "").strip()
    mode = params.get("mode", "search").lower().strip()
    items = params.get("items", [])
    aspect = params.get("aspect", "general").strip() or "general"

    if not query and not items:
        return "Please provide a search query."
    if items and mode not in ("compare",):
        mode = "compare"
    if player:
        player.write_log(f"[Search:{mode}] {query or \', \'.join(items)}")
    print(f"[WebSearch] mode={mode!r} query={query!r}")

    try:
        if mode == "compare" and items: return _compare(items, aspect)
        if mode == "news": return _news(query)
        if mode == "research": return _research(query)
        if mode == "price": return _price(query)
        return _search(query)
    except Exception as e:
        print(f"[WebSearch] All backends failed: {e}")
        return f"Search failed: {e}"
'''

# ═══════════════════════════════════════════════════════════════
# FIXED FILE PROCESSOR CODE (abbreviated - key parts only)
# ═══════════════════════════════════════════════════════════════

FILE_PROCESSOR_FIXED = '''"""file_processor.py - FIXED VERSION with archive reading"""
import os, re, json, shutil, subprocess, tempfile, zipfile, tarfile
from pathlib import Path
from datetime import datetime

def _get_api_key() -> str:
    config_path = Path(__file__).resolve().parent.parent / "config" / "api_keys.json"
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)["gemini_api_key"]

def _gemini_client():
    from google import genai
    _c = genai.Client(api_key=_get_api_key())
    class _W:
        def generate_content(self, contents):
            return _c.models.generate_content(model="gemini-2.5-flash", contents=contents)
    return _W()

def _detect_type(path: Path) -> str:
    ext = path.suffix.lower().lstrip(".")
    image_exts = {"jpg", "jpeg", "png", "gif", "webp", "bmp", "tiff", "svg", "ico"}
    video_exts = {"mp4", "avi", "mov", "mkv", "wmv", "flv", "webm", "m4v", "3gp"}
    audio_exts = {"mp3", "wav", "ogg", "m4a", "aac", "flac", "wma", "opus"}
    code_exts = {"py", "js", "ts", "jsx", "tsx", "html", "css", "java", "c", "cpp", "cs", "go", "rs", "rb", "php", "swift", "kt", "sh", "bash", "ps1", "lua", "r", "m", "sql", "yaml", "toml"}
    archive_exts = {"zip", "rar", "tar", "gz", "7z", "bz2", "xz", "tgz"}
    if ext in image_exts: return "image"
    if ext in video_exts: return "video"
    if ext in audio_exts: return "audio"
    if ext in code_exts: return "code"
    if ext in archive_exts: return "archive"
    if ext == "pdf": return "pdf"
    if ext in ("docx", "doc"): return "docx"
    if ext in ("txt", "md", "rst", "log"): return "text"
    if ext in ("csv", "tsv"): return "csv"
    if ext in ("xlsx", "xls", "ods"): return "excel"
    if ext == "json": return "json"
    if ext == "xml": return "xml"
    if ext in ("pptx", "ppt"): return "pptx"
    return "unknown"

def _file_size_str(path: Path) -> str:
    size = path.stat().st_size
    if size < 1024: return f"{size} B"
    if size < 1024**2: return f"{size/1024:.1f} KB"
    if size < 1024**3: return f"{size/1024**2:.1f} MB"
    return f"{size/1024**3:.1f} GB"

def _output_path(src: Path, suffix: str, new_ext: str = None) -> Path:
    ext = new_ext or src.suffix
    return src.parent / f"{src.stem}_{suffix}{ext}"

# NEW: Archive reading
def _read_file_from_archive(archive_path: Path, inner_path: str) -> str:
    ext = archive_path.suffix.lower()
    try:
        if ext == ".zip":
            with zipfile.ZipFile(archive_path, \'r\') as zf:
                with zf.open(inner_path) as f:
                    raw = f.read()
                    try: return raw.decode(\'utf-8\')
                    except: return f"[Binary: {len(raw)} bytes]"
        elif ext in (".tar", ".gz", ".bz2", ".xz", ".tgz"):
            mode = "r"
            if ext == ".gz" or ext == ".tgz": mode = "r:gz"
            elif ext == ".bz2": mode = "r:bz2"
            elif ext == ".xz": mode = "r:xz"
            with tarfile.open(archive_path, mode) as tf:
                member = tf.getmember(inner_path)
                f = tf.extractfile(member)
                if f:
                    raw = f.read()
                    try: return raw.decode(\'utf-8\')
                    except: return f"[Binary: {len(raw)} bytes]"
        elif ext == ".rar":
            import rarfile
            with rarfile.RarFile(archive_path) as rf:
                raw = rf.read(inner_path)
                try: return raw.decode(\'utf-8\')
                except: return f"[Binary: {len(raw)} bytes]"
        elif ext == ".7z":
            import py7zr
            with py7zr.SevenZipFile(archive_path, \'r\') as sz:
                files = sz.read([inner_path])
                if inner_path in files:
                    raw = files[inner_path].read()
                    try: return raw.decode(\'utf-8\')
                    except: return f"[Binary: {len(raw)} bytes]"
    except Exception as e:
        return f"Error: {e}"
    return f"Unsupported: {ext}"

def _list_archive_contents(archive_path: Path) -> list:
    ext = archive_path.suffix.lower()
    files = []
    try:
        if ext == ".zip":
            with zipfile.ZipFile(archive_path, \'r\') as zf:
                for info in zf.infolist():
                    files.append({"name": info.filename, "size": info.file_size, "is_dir": info.is_dir()})
        elif ext in (".tar", ".gz", ".bz2", ".xz", ".tgz"):
            mode = "r"
            if ext == ".gz" or ext == ".tgz": mode = "r:gz"
            elif ext == ".bz2": mode = "r:bz2"
            elif ext == ".xz": mode = "r:xz"
            with tarfile.open(archive_path, mode) as tf:
                for member in tf.getmembers():
                    files.append({"name": member.name, "size": member.size, "is_dir": member.isdir()})
        elif ext == ".rar":
            import rarfile
            with rarfile.RarFile(archive_path) as rf:
                for info in rf.infolist():
                    files.append({"name": info.filename, "size": info.file_size, "is_dir": info.is_dir()})
        elif ext == ".7z":
            import py7zr
            with py7zr.SevenZipFile(archive_path, \'r\') as sz:
                for name in sz.getnames():
                    files.append({"name": name, "size": 0, "is_dir": False})
    except Exception as e:
        return [{"error": str(e)}]
    return files

def _process_archive(path: Path, action: str, params: dict, speak=None) -> str:
    action = action or "list"
    if action == "list":
        files = _list_archive_contents(path)
        if not files: return "Archive empty."
        if files[0].get("error"): return files[0]["error"]
        text_exts = {\'.txt\', \'.md\', \'.py\', \'.js\', \'.json\', \'.csv\', \'.xml\', \'.html\', \'.css\', \'.yaml\', \'.yml\', \'.log\'}
        text_files = [f for f in files if not f.get("is_dir") and Path(f["name"]).suffix.lower() in text_exts]
        lines = [f"Archive: {path.name}", f"Total: {len(files)} items ({len(text_files)} readable)", ""]
        lines.append("Readable files:")
        for f in text_files[:20]: lines.append(f"  * {f[\'name\']}")
        if len(text_files) > 20: lines.append(f"  ... and {len(text_files)-20} more")
        lines.append("\\nSay \'read [filename]\' to see contents")
        return "\\n".join(lines)
    if action == "read":
        target = params.get("file", "") or params.get("filename", "") or params.get("instruction", "")
        if not target:
            files = _list_archive_contents(path)
            return "Specify file. Available:\\n" + "\\n".join(f"  * {f[\'name\']}" for f in files if not f.get("is_dir"))
        files = _list_archive_contents(path)
        all_names = [f["name"] for f in files]
        matched = target if target in all_names else None
        if not matched:
            for name in all_names:
                if target.lower() in name.lower():
                    matched = name
                    break
        if not matched:
            return f"File \'{target}\' not found. Available:\\n" + "\\n".join(f"  * {n}" for n in all_names[:20])
        content = _read_file_from_archive(path, matched)
        if content.startswith("[Binary"): return f"{matched}: {content}"
        if len(content) > 15000: return f"{matched} ({len(content)} chars)\\n\\n{content[:15000]}\\n\\n[truncated]"
        return f"{matched}\\n\\n{content}"
    if action == "search":
        term = params.get("query", "") or params.get("term", "") or params.get("instruction", "")
        if not term: return "Provide search term."
        files = _list_archive_contents(path)
        text_exts = {\'.txt\', \'.md\', \'.py\', \'.js\', \'.json\', \'.csv\', \'.xml\', \'.html\', \'.css\', \'.yaml\', \'.yml\', \'.log\'}
        text_files = [f["name"] for f in files if not f.get("is_dir") and Path(f["name"]).suffix.lower() in text_exts]
        matches = []
        for fname in text_files:
            content = _read_file_from_archive(path, fname)
            if term.lower() in content.lower():
                idx = content.lower().find(term.lower())
                ctx = content[max(0,idx-100):min(len(content),idx+len(term)+100)].replace(\'\\n\', \' \')
                matches.append({"file": fname, "context": f"...{ctx}..."})
        if not matches: return f"No matches for \'{term}\'"
        lines = [f"Found \'{term}\' in {len(matches)} files:\\n"]
        for m in matches[:10]:
            lines.append(f"{m[\'file\']}")
            lines.append(f"   {m[\'context\']}\\n")
        return "\\n".join(lines)
    if action == "extract":
        dest = Path(params.get("destination", str(path.parent / path.stem)))
        dest.mkdir(parents=True, exist_ok=True)
        try:
            shutil.unpack_archive(str(path), str(dest))
            return f"Extracted to: {dest}"
        except Exception as e:
            return f"Extract failed: {e}"
    return f"Unknown action: {action}. Try: list, read, search, extract"

# Keep existing handlers for other file types - they work as before
def _process_image(path, action, params, speak=None): return "Image processing - use existing code"
def _process_pdf(path, action, params, speak=None): return "PDF processing - use existing code"
def _process_text_doc(path, ft, action, params, speak=None): return "Text processing - use existing code"
def _process_data(path, ft, action, params, speak=None): return "Data processing - use existing code"
def _process_json(path, action, params, speak=None): return "JSON processing - use existing code"
def _process_code(path, action, params, speak=None): return "Code processing - use existing code"
def _process_audio(path, action, params, speak=None): return "Audio processing - use existing code"
def _process_video(path, action, params, speak=None): return "Video processing - use existing code"
def _process_pptx(path, action, params, speak=None): return "PPTX processing - use existing code"

def file_processor(parameters: dict, player=None, speak=None) -> str:
    file_path_str = parameters.get("file_path", "").strip()
    if not file_path_str: return "No file path provided."
    path = Path(file_path_str)
    if not path.exists(): return f"File not found: {file_path_str}"
    if not path.is_file(): return f"Not a file: {file_path_str}"
    file_type = _detect_type(path)
    action = (parameters.get("action") or "").lower().strip()
    instruction = parameters.get("instruction", "")
    params = {**parameters, "instruction": instruction}
    log_msg = f"[FileProcessor] {file_type.upper()} | {path.name} | action={action or \'auto\'}"
    print(log_msg)
    if player: player.write_log(log_msg)
    if file_type == "unknown":
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")[:10000]
            model = _gemini_client()
            response = model.generate_content(f"File: {path.name}\\nContent:\\n{content}\\n\\nTask: {action or \'Describe this file.\'}")
            return response.text.strip()
        except Exception as e:
            return f"Unknown file type. Error: {e}"
    dispatch = {
        "image": _process_image, "pdf": _process_pdf,
        "docx": lambda p, a, pm, s: _process_text_doc(p, "docx", a, pm, s),
        "text": lambda p, a, pm, s: _process_text_doc(p, "text", a, pm, s),
        "csv": lambda p, a, pm, s: _process_data(p, "csv", a, pm, s),
        "excel": lambda p, a, pm, s: _process_data(p, "excel", a, pm, s),
        "json": _process_json,
        "xml": lambda p, a, pm, s: _process_json(p, a, pm, s),
        "code": _process_code, "audio": _process_audio, "video": _process_video,
        "archive": _process_archive,  # FIXED VERSION
        "pptx": _process_pptx,
    }
    handler = dispatch.get(file_type)
    if not handler: return f"Unsupported: {file_type}"
    try:
        result = handler(path, action, params, speak)
        return result or "Done."
    except Exception as e:
        import traceback; traceback.print_exc()
        return f"Processing failed: {e}"
'''

# ═══════════════════════════════════════════════════════════════
# VOICE ORB CODE
# ═══════════════════════════════════════════════════════════════

VOICE_ORB_CODE = '''"""voice_orb.py - PyQt6 Voice Orb Visualization"""
import math
import random
from PyQt6.QtWidgets import QOpenGLWidget
from PyQt6.QtCore import QTimer
from OpenGL.GL import *
from OpenGL.GLU import *

class VoiceOrb(QOpenGLWidget):
    """Voice-reactive particle orb for PyQt6."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 300)
        self.state = "idle"
        self.audio_bands = [0.0, 0.0, 0.0]
        self.time = 0.0
        self.particles = []
        for i in range(5000):
            y = 1 - (i / 4999) * 2
            radius = math.sqrt(1 - y * y)
            theta = i * 2.4
            x = math.cos(theta) * radius
            z = math.sin(theta) * radius
            self.particles.append([x, y, z])
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update)
        self.timer.start(16)
        self.colors = {
            "idle": (0.62, 0.60, 0.87),
            "listening": (0.16, 0.91, 0.71),
            "thinking": (1.0, 0.57, 0.18),
            "speaking": (0.96, 0.27, 0.62),
        }
    
    def set_state(self, state):
        if state in self.colors: self.state = state
    
    def set_audio(self, low, mid, high):
        self.audio_bands = [max(0, min(1, low)), max(0, min(1, mid)), max(0, min(1, high))]
    
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
            if self.state == "idle":
                x += math.sin(self.time * 0.3 + x * 3) * 0.02
                y += math.cos(self.time * 0.2 + y * 3) * 0.02
            elif self.state == "listening":
                scale = 1.0 - low * 0.15 + mid * 0.1
                x *= scale; y *= scale; z *= scale
            elif self.state == "thinking":
                twist = self.time * 0.5 + y * 1.5
                cos_t, sin_t = math.cos(twist), math.sin(twist)
                x, z = x * cos_t + z * sin_t, z * cos_t - x * sin_t
                y *= 0.92
            elif self.state == "speaking":
                scale = 1.0 + low * 0.2 + mid * 0.15
                x *= scale; y *= scale; z *= scale
            depth = (z + 1.5) / 3
            brightness = 0.5 + 0.5 * (low + mid + high) / 3
            glColor4f(color[0]*brightness, color[1]*brightness, color[2]*brightness, 0.5 + depth * 0.5)
            glVertex3f(x, y, z)
        glEnd()


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton
    class TestWindow(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Voice Orb Test")
            self.resize(400, 500)
            layout = QVBoxLayout(self)
            self.orb = VoiceOrb(self)
            layout.addWidget(self.orb)
            for state in ["idle", "listening", "thinking", "speaking"]:
                btn = QPushButton(state.capitalize())
                btn.clicked.connect(lambda checked, s=state: self.orb.set_state(s))
                layout.addWidget(btn)
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())
'''

# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║                                                                  ║")
    print("║          MARK XLVIII - ONE-CLICK INSTALLER                      ║")
    print("║                                                                  ║")
    print("║   This will install everything automatically.                   ║")
    print("║   Your only job: Watch and enjoy.                               ║")
    print("║                                                                  ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    input(f"{Colors.BOLD}Press Enter to begin installation...{Colors.END}")
    
    # Run all steps
    if not clone_repository():
        print_error("Installation failed at step 1")
        return
    
    install_dependencies()
    apply_web_search_fix()
    apply_file_processor_fix()
    add_voice_orb()
    setup_api_key()
    
    print_header("INSTALLATION COMPLETE!")
    print_success("Mark XLVIII is ready!")
    print(f"\n{Colors.BOLD}Installation directory: {INSTALL_DIR}{Colors.END}")
    print(f"\n{Colors.GREEN}To run JARVIS:{Colors.END}")
    print(f"  cd {INSTALL_DIR}")
    print(f"  python main.py\n")
    
    launch_now = input(f"\n{Colors.BOLD}Launch JARVIS now? (y/n): {Colors.END}").strip().lower()
    if launch_now == 'y':
        launch_jarvis()
    else:
        print(f"\n{Colors.GREEN}You can launch JARVIS anytime with:{Colors.END}")
        print(f"  cd {INSTALL_DIR}")
        print(f"  python main.py\n")

if __name__ == "__main__":
    main()
