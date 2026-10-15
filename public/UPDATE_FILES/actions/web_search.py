"""
web_search.py — FIXED VERSION with Wikipedia fallback
REPLACE your actions/web_search.py with this file
"""
import json
import sys
import threading
import requests
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

# ═══════════════════════════════════════════════════════════════
# NEW: Wikipedia fallback for factual queries
# ═══════════════════════════════════════════════════════════════
def _wikipedia_search(query: str) -> str:
    """Fallback: search Wikipedia for factual answers."""
    try:
        import wikipediaapi
        wiki = wikipediaapi.Wikipedia(
            user_agent='Mark-XLVII/2.2 (jarvis@local)',
            language='en'
        )
        page = wiki.page(query)
        if page.exists():
            summary = page.summary[:1500]
            return f"From Wikipedia — {page.title}:\n\n{summary}"
        
        # Try search if exact page not found
        search_results = wiki.search(query, 3) if hasattr(wiki, 'search') else []
        if search_results:
            page = wiki.page(search_results[0])
            if page.exists():
                return f"From Wikipedia — {page.title}:\n\n{page.summary[:1500]}"
    except ImportError:
        print("[WebSearch] wikipedia-api not installed. Run: pip install wikipedia-api")
    except Exception as e:
        print(f"[WebSearch] Wikipedia failed: {e}")
    
    # Second fallback: Wikipedia REST API via requests
    try:
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={requests.utils.quote(query)}&format=json&srlimit=1"
        resp = requests.get(search_url, timeout=5)
        data = resp.json()
        if data.get("query", {}).get("search"):
            title = data["query"]["search"][0]["title"]
            summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(title)}"
            summary_resp = requests.get(summary_url, timeout=5)
            summary_data = summary_resp.json()
            if summary_data.get("extract"):
                return f"From Wikipedia — {summary_data['title']}:\n\n{summary_data['extract']}"
    except Exception as e:
        print(f"[WebSearch] Wikipedia REST API failed: {e}")
    
    return ""

# ═══════════════════════════════════════════════════════════════
# NEW: Smart query enhancement for factual questions
# ═══════════════════════════════════════════════════════════════
def _enhance_query(query: str) -> str:
    """Add context for factual queries."""
    factual_keywords = ["who", "what", "when", "where", "which", "president", 
                        "capital", "population", "prime minister", "king", "queen"]
    query_lower = query.lower()
    
    if any(kw in query_lower for kw in factual_keywords):
        if "current" not in query_lower and "today" not in query_lower:
            time_words = ["president", "leader", "price", "weather", "king", "queen", "prime minister"]
            if any(word in query_lower for word in time_words):
                query = f"current {query}"
    
    return query

def _format_ddg(query: str, results: list[dict]) -> str:
    if not results:
        return f"No results found for: {query}"
    lines = [f"Search results for: {query}\n"]
    for i, r in enumerate(results, 1):
        if r.get("title"):   lines.append(f"{i}. {r['title']}")
        if r.get("snippet"): lines.append(f"   {r['snippet']}")
        if r.get("url"):     lines.append(f"   Source: {r['url']}")
        lines.append("")
    return "\n".join(lines).strip()

def _format_news(query: str, results: list[dict]) -> str:
    if not results:
        return f"No news found for: {query}"
    lines = [f"Latest news: {query}\n"]
    for i, r in enumerate(results, 1):
        title = r.get("title", "")
        if not title:
            continue
        src = f"  [{r['source']}]" if r.get("source") else ""
        lines.append(f"{i}. {title}{src}")
        if r.get("snippet"):
            lines.append(f"   {r['snippet'][:140]}")
        if r.get("url"):
            lines.append(f"   {r['url']}")
        lines.append("")
    return "\n".join(lines).strip()

# ═══════════════════════════════════════════════════════════════
# FIXED: Triple fallback search
# ═══════════════════════════════════════════════════════════════
def _search(query: str) -> str:
    """Triple fallback: Gemini → DDG → Wikipedia"""
    enhanced_query = _enhance_query(query)
    
    # 1. Try Gemini
    try:
        return _gemini_search(enhanced_query)
    except Exception as e:
        print(f"[WebSearch] Gemini failed ({e}) — trying DDG...")
    
    # 2. Try DuckDuckGo
    try:
        results = _ddg_search(enhanced_query)
        if results:
            return _format_ddg(enhanced_query, results)
    except Exception as e:
        print(f"[WebSearch] DDG failed ({e}) — trying Wikipedia...")
    
    # 3. Try Wikipedia (NEW!)
    wiki_result = _wikipedia_search(query)
    if wiki_result:
        return wiki_result
    
    return f"Unable to find information for: {query}"

def _news(query: str) -> str:
    gemini_query = f"latest news today: {query}" if query else "top world news today"
    ddg_query    = query if query else "world news today"
    result_box  = [None]
    lock        = threading.Lock()
    done_evt    = threading.Event()
    failures    = [0]

    def _store(r: str) -> None:
        if r and len(r) > 60:
            with lock:
                if result_box[0] is None:
                    result_box[0] = r
            done_evt.set()
        else:
            with lock:
                failures[0] += 1
                if failures[0] >= 2:
                    done_evt.set()

    def _try_gemini():
        try:
            _store(_gemini_search(gemini_query))
        except Exception as e:
            print(f"[WebSearch] Gemini news failed ({e})")
            _store("")

    def _try_ddg():
        try:
            results = _ddg_news(ddg_query, max_results=8)
            _store(_format_news(ddg_query, results))
        except Exception as e:
            print(f"[WebSearch] DDG news failed ({e})")
            _store("")

    threading.Thread(target=_try_gemini, daemon=True).start()
    threading.Thread(target=_try_ddg,    daemon=True).start()
    done_evt.wait(timeout=10.0)
    return result_box[0] or f"No news found for: {query}"

def _research(query: str) -> str:
    research_query = (
        f"Comprehensive, detailed explanation of: {query}. "
        "Include background context, key facts, current state."
    )
    try:
        return _gemini_search(research_query)
    except Exception as e:
        print(f"[WebSearch] Research Gemini failed ({e})")
        results = _ddg_search(query, max_results=10)
        if results:
            return _format_ddg(query, results)
        wiki = _wikipedia_search(query)
        if wiki:
            return wiki
        return f"Research failed for: {query}"

def _price(query: str) -> str:
    price_query = f"current price of {query} — how much does it cost today"
    try:
        return _gemini_search(price_query)
    except Exception as e:
        print(f"[WebSearch] Price Gemini failed ({e})")
        results = _ddg_search(f"{query} price buy", max_results=6)
        return _format_ddg(query, results)

def _compare(items: list[str], aspect: str) -> str:
    query = f"Compare {', '.join(items)} in terms of {aspect}. Give specific facts."
    try:
        return _gemini_search(query)
    except Exception as e:
        print(f"[WebSearch] Gemini compare failed: {e}")
    all_results: dict[str, list] = {}
    for item in items:
        try:
            all_results[item] = _ddg_search(f"{item} {aspect}", max_results=3)
        except Exception:
            all_results[item] = []
    lines = [f"Comparison — {aspect.upper()}", "─" * 40]
    for item in items:
        lines.append(f"\n▸ {item}")
        for r in all_results.get(item, [])[:2]:
            if r.get("snippet"):
                lines.append(f"  • {r['snippet']}")
            if r.get("url"):
                lines.append(f"    {r['url']}")
    return "\n".join(lines)

# ═══════════════════════════════════════════════════════════════
# Public entry point
# ═══════════════════════════════════════════════════════════════
def web_search(parameters: dict, response=None, player=None, session_memory=None) -> str:
    params = parameters or {}
    query  = params.get("query", "").strip()
    mode   = params.get("mode",  "search").lower().strip()
    items  = params.get("items", [])
    aspect = params.get("aspect", "general").strip() or "general"

    if not query and not items:
        return "Please provide a search query."
    if items and mode not in ("compare",):
        mode = "compare"
    if player:
        player.write_log(f"[Search:{mode}] {query or ', '.join(items)}")
    print(f"[WebSearch] 🔍 mode={mode!r}  query={query!r}")

    try:
        if mode == "compare" and items:
            return _compare(items, aspect)
        if mode == "news":
            return _news(query)
        if mode == "research":
            return _research(query)
        if mode == "price":
            return _price(query)
        return _search(query)
    except Exception as e:
        print(f"[WebSearch] ❌ All backends failed: {e}")
        return f"Search failed: {e}"
