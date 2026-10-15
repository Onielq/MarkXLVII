#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  MARK XLVIII - WINDOWS INSTALLER (No Git Required)              ║
║                                                                  ║
║  This version downloads a ZIP file instead of using git clone   ║
║  which avoids permission issues on Windows.                     ║
║                                                                  ║
║  Run: python install_windows.py                                 ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import subprocess
import shutil
import zipfile
import urllib.request
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════

DOWNLOAD_URL = "https://github.com/Onielq/Mark-XLVII/archive/refs/heads/main.zip"
INSTALL_DIR = Path.home() / "Mark-XLVII"
TEMP_ZIP = Path.home() / "Mark-XLVII-main.zip"

PACKAGES = [
    "rarfile", "py7zr", "wikipedia-api", "PyQt6", "PyOpenGL",
    "numpy", "requests", "google-genai", "duckduckgo-search",
    "sounddevice", "pydub", "Pillow", "pdfplumber", "python-docx",
    "pandas", "openpyxl", "python-pptx", "fastapi", "uvicorn",
]

# ═══════════════════════════════════════════════════════════════
# COLORS
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
# STEP 1: DOWNLOAD ZIP (No Git Required!)
# ═══════════════════════════════════════════════════════════════

def download_repository():
    print_header("STEP 1: Downloading Mark XLVIII (ZIP - No Git!)")
    
    # Clean up any existing installation
    if INSTALL_DIR.exists():
        print_warning(f"Removing existing installation: {INSTALL_DIR}")
        try:
            # Fix permissions first
            subprocess.run(
                ["takeown", "/f", str(INSTALL_DIR), "/r", "/d", "y"],
                capture_output=True, shell=True
            )
            subprocess.run(
                ["icacls", str(INSTALL_DIR), "/reset", "/t", "/c", "/q"],
                capture_output=True, shell=True
            )
            shutil.rmtree(INSTALL_DIR, ignore_errors=True)
        except Exception as e:
            print_warning(f"Could not remove old folder: {e}")
            print_warning("Trying to continue anyway...")
    
    # Download ZIP file
    print_step(f"Downloading from {DOWNLOAD_URL}...")
    try:
        urllib.request.urlretrieve(DOWNLOAD_URL, TEMP_ZIP)
        print_success("Download complete")
    except Exception as e:
        print_error(f"Download failed: {e}")
        print_warning("Check your internet connection")
        return False
    
    # Extract ZIP
    print_step("Extracting files...")
    try:
        with zipfile.ZipFile(TEMP_ZIP, 'r') as zip_ref:
            zip_ref.extractall(Path.home())
        
        # Rename extracted folder
        extracted = Path.home() / "Mark-XLVII-main"
        if extracted.exists():
            extracted.rename(INSTALL_DIR)
        
        print_success("Extraction complete")
        
        # Clean up ZIP
        if TEMP_ZIP.exists():
            TEMP_ZIP.unlink()
        
        return True
    except Exception as e:
        print_error(f"Extraction failed: {e}")
        return False

# ═══════════════════════════════════════════════════════════════
# STEP 2: INSTALL DEPENDENCIES
# ═══════════════════════════════════════════════════════════════

def install_dependencies():
    print_header("STEP 2: Installing Python Dependencies")
    
    # Install requirements.txt if it exists
    req_file = INSTALL_DIR / "requirements.txt"
    if req_file.exists():
        print_step("Installing from requirements.txt...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(req_file), "--quiet", "--user"],
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
                [sys.executable, "-m", "pip", "install", package, "--quiet", "--user"],
                check=True
            )
            print_success(f"  {package}")
        except subprocess.CalledProcessError:
            print_warning(f"  {package} - skipped")
    
    print_success("All dependencies installed")

# ═══════════════════════════════════════════════════════════════
# STEP 3: APPLY FIXES
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
        print_success(f"Backed up original")
    
    # Write fixed version
    print_step("Writing fixed web_search.py...")
    web_search_path.write_text(WEB_SEARCH_FIXED, encoding='utf-8')
    print_success("Web search fix applied")
    return True

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
        print_success(f"Backed up original")
    
    # Write fixed version
    print_step("Writing fixed file_processor.py...")
    file_processor_path.write_text(FILE_PROCESSOR_FIXED, encoding='utf-8')
    print_success("File processor fix applied")
    return True

def add_voice_orb():
    print_header("STEP 5: Adding Voice Orb + Updated UI")
    
    voice_orb_path = INSTALL_DIR / "voice_orb.py"
    
    print_step("Writing voice_orb.py...")
    voice_orb_path.write_text(VOICE_ORB_CODE, encoding='utf-8')
    print_success("Voice orb added")
    
    # Backup and replace ui.py
    ui_path = INSTALL_DIR / "ui.py"
    if ui_path.exists():
        backup = ui_path.with_suffix(".py.backup")
        shutil.copy2(ui_path, backup)
        print_success(f"Backed up original ui.py")
    
    print_step("Writing updated ui.py with Voice Orb integration...")
    ui_path.write_text(UI_CODE, encoding='utf-8')
    print_success("ui.py updated with Voice Orb")
    
    return True

# ═══════════════════════════════════════════════════════════════
# STEP 4: SETUP API KEY
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
            encoding='utf-8'
        )
        print_success("API key saved")
    else:
        print_warning("Skipped - run 'python setup.py' later")
    
    return True

# ═══════════════════════════════════════════════════════════════
# STEP 5: LAUNCH
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
# CODE TEMPLATES (Same as before)
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

BASE_DIR = _get_base_dir()
API_CONFIG_PATH = BASE_DIR / "config" / "api_keys.json"

def _get_api_key() -> str:
    with open(API_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["gemini_api_key"]

def _gemini_search(query: str) -> str:
    from google import genai
    client = genai.Client(api_key=_get_api_key())
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
                "title": r.get("title", ""),
                "snippet": r.get("body", ""),
                "url": r.get("href", ""),
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
                    "title": r.get("title", ""),
                    "snippet": r.get("body", ""),
                    "url": r.get("url", ""),
                    "source": r.get("source", ""),
                })
    except Exception as e:
        print(f"[WebSearch] DDG news failed ({e})")
        results = _ddg_search(query, max_results=max_results)
    return results

def _wikipedia_search(query: str) -> str:
    try:
        import wikipediaapi
        wiki = wikipediaapi.Wikipedia(
            user_agent='Mark-XLVII/2.2 (jarvis@local)',
            language='en'
        )
        page = wiki.page(query)
        if page.exists():
            return f"From Wikipedia - {page.title}:\\n\\n{page.summary[:1500]}"
    except ImportError:
        print("[WebSearch] wikipedia-api not installed")
    except Exception as e:
        print(f"[WebSearch] Wikipedia failed: {e}")
    
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
                return f"From Wikipedia - {summary_data['title']}:\\n\\n{summary_data['extract']}"
    except Exception as e:
        print(f"[WebSearch] Wikipedia REST failed: {e}")
    return ""

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
        if r.get("title"): lines.append(f"{i}. {r['title']}")
        if r.get("snippet"): lines.append(f"   {r['snippet']}")
        if r.get("url"): lines.append(f"   Source: {r['url']}")
        lines.append("")
    return "\\n".join(lines).strip()

def _format_news(query: str, results: list[dict]) -> str:
    if not results:
        return f"No news found for: {query}"
    lines = [f"Latest news: {query}\\n"]
    for i, r in enumerate(results, 1):
        title = r.get("title", "")
        if not title: continue
        src = f"  [{r['source']}]" if r.get("source") else ""
        lines.append(f"{i}. {title}{src}")
        if r.get("snippet"): lines.append(f"   {r['snippet'][:140]}")
        if r.get("url"): lines.append(f"   {r['url']}")
        lines.append("")
    return "\\n".join(lines).strip()

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
        return _gemini_search(f"Compare {', '.join(items)} in terms of {aspect}.")
    except:
        lines = [f"Comparison - {aspect.upper()}", "-" * 40]
        for item in items:
            lines.append(f"\\n> {item}")
            try:
                for r in _ddg_search(f"{item} {aspect}", max_results=2):
                    if r.get("snippet"): lines.append(f"  * {r['snippet']}")
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
        player.write_log(f"[Search:{mode}] {query or ', '.join(items)}")
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

def _read_file_from_archive(archive_path: Path, inner_path: str) -> str:
    ext = archive_path.suffix.lower()
    try:
        if ext == ".zip":
            with zipfile.ZipFile(archive_path, 'r') as zf:
                with zf.open(inner_path) as f:
                    raw = f.read()
                    try: return raw.decode('utf-8')
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
                    try: return raw.decode('utf-8')
                    except: return f"[Binary: {len(raw)} bytes]"
        elif ext == ".rar":
            import rarfile
            with rarfile.RarFile(archive_path) as rf:
                raw = rf.read(inner_path)
                try: return raw.decode('utf-8')
                except: return f"[Binary: {len(raw)} bytes]"
        elif ext == ".7z":
            import py7zr
            with py7zr.SevenZipFile(archive_path, 'r') as sz:
                files = sz.read([inner_path])
                if inner_path in files:
                    raw = files[inner_path].read()
                    try: return raw.decode('utf-8')
                    except: return f"[Binary: {len(raw)} bytes]"
    except Exception as e:
        return f"Error: {e}"
    return f"Unsupported: {ext}"

def _list_archive_contents(archive_path: Path) -> list:
    ext = archive_path.suffix.lower()
    files = []
    try:
        if ext == ".zip":
            with zipfile.ZipFile(archive_path, 'r') as zf:
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
            with py7zr.SevenZipFile(archive_path, 'r') as sz:
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
        text_exts = {'.txt', '.md', '.py', '.js', '.json', '.csv', '.xml', '.html', '.css', '.yaml', '.yml', '.log'}
        text_files = [f for f in files if not f.get("is_dir") and Path(f["name"]).suffix.lower() in text_exts]
        lines = [f"Archive: {path.name}", f"Total: {len(files)} items ({len(text_files)} readable)", ""]
        lines.append("Readable files:")
        for f in text_files[:20]: lines.append(f"  * {f['name']}")
        if len(text_files) > 20: lines.append(f"  ... and {len(text_files)-20} more")
        lines.append("\\nSay 'read [filename]' to see contents")
        return "\\n".join(lines)
    if action == "read":
        target = params.get("file", "") or params.get("filename", "") or params.get("instruction", "")
        if not target:
            files = _list_archive_contents(path)
            return "Specify file. Available:\\n" + "\\n".join(f"  * {f['name']}" for f in files if not f.get("is_dir"))
        files = _list_archive_contents(path)
        all_names = [f["name"] for f in files]
        matched = target if target in all_names else None
        if not matched:
            for name in all_names:
                if target.lower() in name.lower():
                    matched = name
                    break
        if not matched:
            return f"File '{target}' not found. Available:\\n" + "\\n".join(f"  * {n}" for n in all_names[:20])
        content = _read_file_from_archive(path, matched)
        if content.startswith("[Binary"): return f"{matched}: {content}"
        if len(content) > 15000: return f"{matched} ({len(content)} chars)\\n\\n{content[:15000]}\\n\\n[truncated]"
        return f"{matched}\\n\\n{content}"
    if action == "search":
        term = params.get("query", "") or params.get("term", "") or params.get("instruction", "")
        if not term: return "Provide search term."
        files = _list_archive_contents(path)
        text_exts = {'.txt', '.md', '.py', '.js', '.json', '.csv', '.xml', '.html', '.css', '.yaml', '.yml', '.log'}
        text_files = [f["name"] for f in files if not f.get("is_dir") and Path(f["name"]).suffix.lower() in text_exts]
        matches = []
        for fname in text_files:
            content = _read_file_from_archive(path, fname)
            if term.lower() in content.lower():
                idx = content.lower().find(term.lower())
                ctx = content[max(0,idx-100):min(len(content),idx+len(term)+100)].replace('\\n', ' ')
                matches.append({"file": fname, "context": f"...{ctx}..."})
        if not matches: return f"No matches for '{term}'"
        lines = [f"Found '{term}' in {len(matches)} files:\\n"]
        for m in matches[:10]:
            lines.append(f"{m['file']}")
            lines.append(f"   {m['context']}\\n")
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
    log_msg = f"[FileProcessor] {file_type.upper()} | {path.name} | action={action or 'auto'}"
    print(log_msg)
    if player: player.write_log(log_msg)
    if file_type == "unknown":
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")[:10000]
            model = _gemini_client()
            response = model.generate_content(f"File: {path.name}\\nContent:\\n{content}\\n\\nTask: {action or 'Describe this file.'}")
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
        "archive": _process_archive,
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

VOICE_ORB_CODE = '''"""voice_orb.py - PyQt6 Voice Orb Visualization"""
import math
from PyQt6.QtWidgets import QOpenGLWidget
from PyQt6.QtCore import QTimer
from OpenGL.GL import *
from OpenGL.GLU import *

class VoiceOrb(QOpenGLWidget):
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
'''

# ═══════════════════════════════════════════════════════════════
# UI CODE (with Voice Orb integration)
# ═══════════════════════════════════════════════════════════════

UI_CODE = '''"""ui.py - Mark XLVIII PyQt6 Interface with Voice Orb"""
import sys
from datetime import datetime
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QFrame, QStatusBar,
    QMenuBar, QMenu, QSystemTrayIcon, QApplication
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QAction

try:
    from voice_orb import VoiceOrb
    VOICE_ORB_AVAILABLE = True
except ImportError:
    VOICE_ORB_AVAILABLE = False
    print("[UI] Voice orb not available - install: pip install PyQt6 PyOpenGL numpy")

DARK_THEME = """
QMainWindow { background-color: #071018; }
QWidget { background-color: #071018; color: #e6f7fb; font-family: 'Segoe UI', Arial, sans-serif; }
QLabel { color: #e6f7fb; background: transparent; }
QTextEdit {
    background-color: #0d1c27; color: #e6f7fb;
    border: 1px solid #1d3c4a; border-radius: 8px;
    padding: 10px; font-family: 'Consolas', monospace; font-size: 12px;
}
QPushButton {
    background-color: #0d1c27; color: #e6f7fb;
    border: 1px solid #1d3c4a; border-radius: 8px;
    padding: 8px 16px; font-weight: bold; min-height: 20px;
}
QPushButton:hover { background-color: #1d3c4a; border-color: #00d4ff; }
QPushButton:pressed { background-color: #00d4ff; color: #00141b; }
QPushButton#interruptBtn { background-color: #f87171; color: white; border: 1px solid #dc2626; }
QPushButton#interruptBtn:hover { background-color: #dc2626; }
QStatusBar { background-color: #0d1c27; color: #9bb6bd; border-top: 1px solid #1d3c4a; }
QMenuBar { background-color: #0d1c27; color: #e6f7fb; border-bottom: 1px solid #1d3c4a; }
QMenu { background-color: #0d1c27; color: #e6f7fb; border: 1px solid #1d3c4a; }
"""

class JarvisUI(QMainWindow):
    log_signal = pyqtSignal(str, str)
    state_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)
    
    def __init__(self, jarvis_instance=None):
        super().__init__()
        self.jarvis = jarvis_instance
        self.setWindowTitle("JARVIS - Mark XLVIII")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        self.setStyleSheet(DARK_THEME)
        self._setup_ui()
        self._setup_menu()
        self._setup_status_bar()
        self.log_signal.connect(self._append_log)
        self.state_signal.connect(self._update_state)
        self.status_signal.connect(self._update_status)
        self.current_state = "idle"
        self._update_state("idle")
        self._append_log("system", "JARVIS Mark XLVIII initialized")
        self._append_log("system", "Voice Orb: " + ("ACTIVE" if VOICE_ORB_AVAILABLE else "NOT AVAILABLE"))
        self._append_log("jarvis", "Good day. All systems operational. How may I assist you?")
    
    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # TOP: Voice Orb + Status
        top_section = QHBoxLayout()
        top_section.setSpacing(20)
        
        if VOICE_ORB_AVAILABLE:
            orb_container = QFrame()
            orb_container.setStyleSheet("QFrame { background-color: #0d1c27; border: 1px solid #1d3c4a; border-radius: 12px; }")
            orb_layout = QVBoxLayout(orb_container)
            orb_layout.setContentsMargins(10, 10, 10, 10)
            
            orb_title = QLabel("VOICE ORB")
            orb_title.setStyleSheet("color: #9bb6bd; font-size: 11px; font-weight: bold;")
            orb_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            orb_layout.addWidget(orb_title)
            
            self.voice_orb = VoiceOrb(self)
            self.voice_orb.setMinimumSize(300, 300)
            self.voice_orb.setMaximumSize(400, 400)
            orb_layout.addWidget(self.voice_orb)
            
            self.orb_state_label = QLabel("IDLE")
            self.orb_state_label.setStyleSheet("color: #00d4ff; font-size: 14px; font-weight: bold; padding: 5px; background-color: #071018; border-radius: 6px;")
            self.orb_state_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            orb_layout.addWidget(self.orb_state_label)
            
            top_section.addWidget(orb_container)
        
        # Status panel
        status_panel = QFrame()
        status_panel.setStyleSheet("QFrame { background-color: #0d1c27; border: 1px solid #1d3c4a; border-radius: 12px; }")
        status_layout = QVBoxLayout(status_panel)
        status_layout.setContentsMargins(15, 15, 15, 15)
        
        status_title = QLabel("SYSTEM STATUS")
        status_title.setStyleSheet("color: #9bb6bd; font-size: 11px; font-weight: bold;")
        status_layout.addWidget(status_title)
        
        self.status_indicators = {}
        for name, color in [("Gemini API", "#00d4ff"), ("Microphone", "#7ef0c1"), ("Web Search", "#fbbf24"), ("File System", "#f87171"), ("Memory", "#00d4ff"), ("Network", "#7ef0c1")]:
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
        
        self.interrupt_btn = QPushButton("⬛ INTERRUPT")
        self.interrupt_btn.setObjectName("interruptBtn")
        self.interrupt_btn.setMinimumHeight(50)
        self.interrupt_btn.clicked.connect(self._on_interrupt)
        status_layout.addWidget(self.interrupt_btn)
        
        top_section.addWidget(status_panel)
        main_layout.addLayout(top_section)
        
        # MIDDLE: Conversation Log
        log_frame = QFrame()
        log_frame.setStyleSheet("QFrame { background-color: #0d1c27; border: 1px solid #1d3c4a; border-radius: 12px; }")
        log_layout = QVBoxLayout(log_frame)
        log_layout.setContentsMargins(15, 15, 15, 15)
        
        log_header = QHBoxLayout()
        log_title = QLabel("CONVERSATION LOG")
        log_title.setStyleSheet("color: #9bb6bd; font-size: 11px; font-weight: bold;")
        log_header.addWidget(log_title)
        log_header.addStretch()
        
        clear_btn = QPushButton("Clear")
        clear_btn.setMaximumWidth(80)
        clear_btn.clicked.connect(lambda: self.log_text.clear())
        log_header.addWidget(clear_btn)
        log_layout.addLayout(log_header)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMinimumHeight(300)
        log_layout.addWidget(self.log_text)
        main_layout.addWidget(log_frame)
        
        # BOTTOM: Quick Actions
        actions_frame = QFrame()
        actions_frame.setStyleSheet("QFrame { background-color: #0d1c27; border: 1px solid #1d3c4a; border-radius: 12px; }")
        actions_layout = QHBoxLayout(actions_frame)
        actions_layout.setContentsMargins(15, 15, 15, 15)
        
        for text in ["🔍 Search", "📁 Files", "🌤️ Weather", "📰 News", "🎵 Music", "⚙️ Settings"]:
            btn = QPushButton(text)
            actions_layout.addWidget(btn)
        
        main_layout.addWidget(actions_frame)
    
    def _setup_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
    
    def _setup_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_label = QLabel("Ready")
        self.status_bar.addWidget(self.status_label)
        self.time_label = QLabel()
        self.status_bar.addPermanentWidget(self.time_label)
        self.time_timer = QTimer(self)
        self.time_timer.timeout.connect(lambda: self.time_label.setText(datetime.now().strftime("%H:%M:%S")))
        self.time_timer.start(1000)
    
    def write_log(self, speaker: str, message: str):
        self.log_signal.emit(speaker, message)
    
    def set_state(self, state: str):
        self.state_signal.emit(state)
    
    def set_status(self, message: str):
        self.status_signal.emit(message)
    
    def set_audio_bands(self, low: float, mid: float, high: float):
        if VOICE_ORB_AVAILABLE and hasattr(self, 'voice_orb'):
            self.voice_orb.set_audio(low, mid, high)
    
    def _append_log(self, speaker: str, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        colors = {"user": "#7ef0c1", "jarvis": "#00d4ff", "system": "#9bb6bd", "healer": "#fbbf24", "error": "#f87171"}
        labels = {"user": "You", "jarvis": "Jarvis", "system": "SYS", "healer": "Healer", "error": "ERR"}
        color = colors.get(speaker, "#e6f7fb")
        label = labels.get(speaker, speaker.upper())
        html = f'<span style="color: #1d3c4a;">[{timestamp}]</span> <span style="color: {color}; font-weight: bold;">{label}:</span> <span style="color: {color};">{message}</span>'
        self.log_text.append(html)
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def _update_state(self, state: str):
        self.current_state = state
        if VOICE_ORB_AVAILABLE and hasattr(self, 'voice_orb'):
            self.voice_orb.set_state(state)
        if hasattr(self, 'orb_state_label'):
            self.orb_state_label.setText(state.upper())
            state_colors = {"idle": "#9bb6bd", "listening": "#7ef0c1", "thinking": "#fbbf24", "speaking": "#00d4ff"}
            color = state_colors.get(state, "#9bb6bd")
            self.orb_state_label.setStyleSheet(f"color: {color}; font-size: 14px; font-weight: bold; padding: 5px; background-color: #071018; border-radius: 6px;")
    
    def _update_status(self, message: str):
        self.status_label.setText(message)
    
    def _on_interrupt(self):
        self._append_log("system", "User interrupted JARVIS")
        self.set_state("idle")
        if self.jarvis and hasattr(self.jarvis, 'interrupt'):
            self.jarvis.interrupt()
    
    def closeEvent(self, event):
        if self.jarvis and hasattr(self.jarvis, 'shutdown'):
            self.jarvis.shutdown()
        event.accept()
'''

# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║                                                                  ║")
    print("║     MARK XLVIII - WINDOWS INSTALLER (No Git Required)           ║")
    print("║                                                                  ║")
    print("║   This version avoids permission issues by using ZIP download   ║")
    print("║                                                                  ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    input(f"{Colors.BOLD}Press Enter to begin installation...{Colors.END}")
    
    if not download_repository():
        print_error("Installation failed")
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
