"""
file_processor.py — FIXED VERSION with archive reading
REPLACE your actions/file_processor.py with this file

NEW: Can now read files inside zip/tar/rar/7z without extracting
"""
import os
import re
import json
import shutil
import subprocess
import tempfile
import zipfile
import tarfile
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
    code_exts  = {"py", "js", "ts", "jsx", "tsx", "html", "css", "java", "c",
                  "cpp", "cs", "go", "rs", "rb", "php", "swift", "kt", "sh",
                  "bash", "ps1", "lua", "r", "m", "sql", "yaml", "toml"}
    archive_exts = {"zip", "rar", "tar", "gz", "7z", "bz2", "xz", "tgz"}

    if ext in image_exts:  return "image"
    if ext in video_exts:  return "video"
    if ext in audio_exts:  return "audio"
    if ext in code_exts:   return "code"
    if ext in archive_exts: return "archive"
    if ext == "pdf":       return "pdf"
    if ext in ("docx", "doc"): return "docx"
    if ext in ("txt", "md", "rst", "log"): return "text"
    if ext in ("csv", "tsv"): return "csv"
    if ext in ("xlsx", "xls", "ods"): return "excel"
    if ext == "json":      return "json"
    if ext == "xml":       return "xml"
    if ext in ("pptx", "ppt"): return "pptx"
    return "unknown"

def _file_size_str(path: Path) -> str:
    size = path.stat().st_size
    if size < 1024:        return f"{size} B"
    if size < 1024**2:     return f"{size/1024:.1f} KB"
    if size < 1024**3:     return f"{size/1024**2:.1f} MB"
    return f"{size/1024**3:.1f} GB"

def _output_path(src: Path, suffix: str, new_ext: str = None) -> Path:
    ext  = new_ext or src.suffix
    name = f"{src.stem}_{suffix}{ext}"
    return src.parent / name

# ═══════════════════════════════════════════════════════════════
# NEW: Archive reading functions
# ═══════════════════════════════════════════════════════════════
def _read_file_from_archive(archive_path: Path, inner_path: str) -> str:
    """Read a single file from within an archive."""
    ext = archive_path.suffix.lower()
    
    try:
        if ext == ".zip":
            with zipfile.ZipFile(archive_path, 'r') as zf:
                with zf.open(inner_path) as f:
                    raw = f.read()
                    try:
                        return raw.decode('utf-8')
                    except UnicodeDecodeError:
                        return f"[Binary file: {len(raw)} bytes]"
        
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
                    try:
                        return raw.decode('utf-8')
                    except UnicodeDecodeError:
                        return f"[Binary file: {len(raw)} bytes]"
                return "[Could not extract file]"
        
        elif ext == ".rar":
            try:
                import rarfile
                with rarfile.RarFile(archive_path) as rf:
                    raw = rf.read(inner_path)
                    try:
                        return raw.decode('utf-8')
                    except UnicodeDecodeError:
                        return f"[Binary file: {len(raw)} bytes]"
            except ImportError:
                return "rarfile not installed. Run: pip install rarfile"
        
        elif ext == ".7z":
            try:
                import py7zr
                with py7zr.SevenZipFile(archive_path, 'r') as sz:
                    files = sz.read([inner_path])
                    if inner_path in files:
                        raw = files[inner_path].read()
                        try:
                            return raw.decode('utf-8')
                        except UnicodeDecodeError:
                            return f"[Binary file: {len(raw)} bytes]"
                    return "[File not found in archive]"
            except ImportError:
                return "py7zr not installed. Run: pip install py7zr"
    
    except Exception as e:
        return f"Error reading {inner_path}: {e}"
    
    return f"Unsupported archive format: {ext}"

def _list_archive_contents(archive_path: Path) -> list[dict]:
    """List all files in an archive with metadata."""
    ext = archive_path.suffix.lower()
    files = []
    
    try:
        if ext == ".zip":
            with zipfile.ZipFile(archive_path, 'r') as zf:
                for info in zf.infolist():
                    files.append({
                        "name": info.filename,
                        "size": info.file_size,
                        "is_dir": info.is_dir(),
                    })
        
        elif ext in (".tar", ".gz", ".bz2", ".xz", ".tgz"):
            mode = "r"
            if ext == ".gz" or ext == ".tgz": mode = "r:gz"
            elif ext == ".bz2": mode = "r:bz2"
            elif ext == ".xz": mode = "r:xz"
            
            with tarfile.open(archive_path, mode) as tf:
                for member in tf.getmembers():
                    files.append({
                        "name": member.name,
                        "size": member.size,
                        "is_dir": member.isdir(),
                    })
        
        elif ext == ".rar":
            try:
                import rarfile
                with rarfile.RarFile(archive_path) as rf:
                    for info in rf.infolist():
                        files.append({
                            "name": info.filename,
                            "size": info.file_size,
                            "is_dir": info.is_dir(),
                        })
            except ImportError:
                return [{"error": "rarfile not installed. Run: pip install rarfile"}]
        
        elif ext == ".7z":
            try:
                import py7zr
                with py7zr.SevenZipFile(archive_path, 'r') as sz:
                    for name in sz.getnames():
                        files.append({
                            "name": name,
                            "size": 0,
                            "is_dir": False,
                        })
            except ImportError:
                return [{"error": "py7zr not installed. Run: pip install py7zr"}]
    
    except Exception as e:
        return [{"error": str(e)}]
    
    return files

def _process_archive(path: Path, action: str, params: dict, speak=None) -> str:
    """FIXED: Full archive processing with content reading."""
    action = action or "list"
    
    # List files
    if action == "list":
        files = _list_archive_contents(path)
        if not files:
            return "Archive is empty or could not be read."
        
        if files and files[0].get("error"):
            return files[0]["error"]
        
        text_exts = {'.txt', '.md', '.py', '.js', '.json', '.csv', '.xml', '.html', '.css', '.yaml', '.yml', '.log'}
        text_files = [f for f in files if not f.get("is_dir") and Path(f["name"]).suffix.lower() in text_exts]
        other_files = [f for f in files if not f.get("is_dir") and f not in text_files]
        
        lines = [f"Archive: {path.name}", f"Total: {len(files)} items ({len(text_files)} text, {len(other_files)} other)", ""]
        lines.append("📄 Text files (can be read):")
        for f in text_files[:20]:
            lines.append(f"  • {f['name']}")
        if len(text_files) > 20:
            lines.append(f"  ... and {len(text_files) - 20} more")
        
        if other_files:
            lines.append("")
            lines.append("📦 Other files:")
            for f in other_files[:10]:
                lines.append(f"  • {f['name']}")
        
        lines.append("")
        lines.append("💡 Say 'read [filename]' to see contents")
        return "\n".join(lines)
    
    # Read specific file
    if action == "read":
        target = params.get("file", "") or params.get("filename", "") or params.get("instruction", "")
        if not target:
            files = _list_archive_contents(path)
            text_files = [f["name"] for f in files if not f.get("is_dir")]
            return "Please specify which file. Available:\n" + "\n".join(f"  • {f}" for f in text_files[:20])
        
        # Find file (fuzzy match)
        files = _list_archive_contents(path)
        all_names = [f["name"] for f in files]
        matched = target if target in all_names else None
        
        if not matched:
            target_lower = target.lower()
            for name in all_names:
                if target_lower in name.lower():
                    matched = name
                    break
        
        if not matched:
            return f"File '{target}' not found. Available:\n" + "\n".join(f"  • {n}" for n in all_names[:20])
        
        content = _read_file_from_archive(path, matched)
        if content.startswith("[Binary"):
            return f"{matched}: {content}"
        
        if len(content) > 15000:
            return f"📄 {matched} ({len(content)} chars)\n\n{content[:15000]}\n\n... [truncated]"
        return f"📄 {matched}\n\n{content}"
    
    # Search inside archive
    if action == "search":
        search_term = params.get("query", "") or params.get("term", "") or params.get("instruction", "")
        if not search_term:
            return "Please provide a search term."
        
        files = _list_archive_contents(path)
        text_exts = {'.txt', '.md', '.py', '.js', '.json', '.csv', '.xml', '.html', '.css', '.yaml', '.yml', '.log'}
        text_files = [f["name"] for f in files if not f.get("is_dir") and Path(f["name"]).suffix.lower() in text_exts]
        
        matches = []
        for fname in text_files:
            content = _read_file_from_archive(path, fname)
            if search_term.lower() in content.lower():
                idx = content.lower().find(search_term.lower())
                start = max(0, idx - 100)
                end = min(len(content), idx + len(search_term) + 100)
                context = content[start:end].replace('\n', ' ').strip()
                matches.append({"file": fname, "context": f"...{context}..."})
        
        if not matches:
            return f"No matches for '{search_term}' in {len(text_files)} files."
        
        lines = [f"Found '{search_term}' in {len(matches)} files:\n"]
        for m in matches[:10]:
            lines.append(f"📄 {m['file']}")
            lines.append(f"   {m['context']}\n")
        return "\n".join(lines)
    
    # Extract
    if action == "extract":
        dest = Path(params.get("destination", str(path.parent / path.stem)))
        dest.mkdir(parents=True, exist_ok=True)
        try:
            shutil.unpack_archive(str(path), str(dest))
            return f"Extracted to: {dest}"
        except Exception as e:
            return f"Extract failed: {e}"
    
    return f"Unknown action: '{action}'. Try: list, read, search, extract"

# ═══════════════════════════════════════════════════════════════
# Other file processors (abbreviated - keep your existing ones)
# ═══════════════════════════════════════════════════════════════
def _process_image(path: Path, action: str, params: dict, speak=None) -> str:
    # Keep your existing image processing code here
    return "Image processing not shown - use your existing code"

def _process_pdf(path: Path, action: str, params: dict, speak=None) -> str:
    # Keep your existing PDF processing code here
    return "PDF processing not shown - use your existing code"

def _process_text_doc(path: Path, file_type: str, action: str, params: dict, speak=None) -> str:
    # Keep your existing text processing code here
    return "Text processing not shown - use your existing code"

def _process_data(path: Path, file_type: str, action: str, params: dict, speak=None) -> str:
    # Keep your existing data processing code here
    return "Data processing not shown - use your existing code"

def _process_json(path: Path, action: str, params: dict, speak=None) -> str:
    # Keep your existing JSON processing code here
    return "JSON processing not shown - use your existing code"

def _process_code(path: Path, action: str, params: dict, speak=None) -> str:
    # Keep your existing code processing code here
    return "Code processing not shown - use your existing code"

def _process_audio(path: Path, action: str, params: dict, speak=None) -> str:
    # Keep your existing audio processing code here
    return "Audio processing not shown - use your existing code"

def _process_video(path: Path, action: str, params: dict, speak=None) -> str:
    # Keep your existing video processing code here
    return "Video processing not shown - use your existing code"

def _process_pptx(path: Path, action: str, params: dict, speak=None) -> str:
    # Keep your existing PPTX processing code here
    return "PPTX processing not shown - use your existing code"

# ═══════════════════════════════════════════════════════════════
# Main entry point
# ═══════════════════════════════════════════════════════════════
def file_processor(parameters: dict, player=None, speak=None) -> str:
    file_path_str = parameters.get("file_path", "").strip()
    if not file_path_str:
        return "No file path provided."

    path = Path(file_path_str)
    if not path.exists():
        return f"File not found: {file_path_str}"
    if not path.is_file():
        return f"Path is not a file: {file_path_str}"

    file_type   = _detect_type(path)
    action      = (parameters.get("action") or "").lower().strip()
    instruction = parameters.get("instruction", "")
    params      = {**parameters, "instruction": instruction}

    log_msg = f"[FileProcessor] {file_type.upper()} | {path.name} | action={action or 'auto'}"
    print(log_msg)
    if player:
        player.write_log(log_msg)

    if file_type == "unknown":
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")[:10000]
            model   = _gemini_client()
            prompt  = f"File: {path.name}\nContent:\n{content}\n\nTask: {action or instruction or 'Describe this file.'}"
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Unknown file type. Error: {e}"

    dispatch = {
        "image":   _process_image,
        "pdf":     _process_pdf,
        "docx":    lambda p, a, pm, s: _process_text_doc(p, "docx", a, pm, s),
        "text":    lambda p, a, pm, s: _process_text_doc(p, "text", a, pm, s),
        "csv":     lambda p, a, pm, s: _process_data(p, "csv",   a, pm, s),
        "excel":   lambda p, a, pm, s: _process_data(p, "excel", a, pm, s),
        "json":    _process_json,
        "xml":     lambda p, a, pm, s: _process_json(p, a, pm, s),
        "code":    _process_code,
        "audio":   _process_audio,
        "video":   _process_video,
        "archive": _process_archive,  # ← FIXED VERSION
        "pptx":    _process_pptx,
    }

    handler = dispatch.get(file_type)
    if not handler:
        return f"Unsupported file type: {file_type}"

    try:
        result = handler(path, action, params, speak)
        return result or "Done."
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Processing failed: {e}"
