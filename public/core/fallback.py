"""
core/fallback.py - Multi-Level Fallback Management

Manages fallback chains for various services.
"""

import asyncio
from pathlib import Path
from typing import Dict, Any, Optional


class FallbackManager:
    """
    Manages multi-level fallback chains.
    Activates fallbacks when primary systems fail.
    """
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.active_fallbacks = {}
        self.fallback_chains = self._setup_fallback_chains()
    
    async def activate(self, fallback_id: str) -> bool:
        """Activate a fallback system."""
        if fallback_id not in self.fallback_chains:
            return False
        
        chain = self.fallback_chains[fallback_id]
        
        for fallback in chain:
            try:
                success = await self._try_fallback(fallback)
                if success:
                    self.active_fallbacks[fallback_id] = fallback
                    return True
            except Exception:
                continue
        
        return False
    
    async def _try_fallback(self, fallback: Dict) -> bool:
        """Try to activate a specific fallback."""
        fallback_type = fallback.get("type")
        
        if fallback_type == "search_fallback":
            return await self._activate_search_fallback()
        elif fallback_type == "wikipedia_fallback":
            return await self._activate_wikipedia_fallback()
        elif fallback_type == "api_endpoint":
            return await self._activate_api_fallback()
        elif fallback_type == "dns_fallback":
            return await self._activate_dns_fallback()
        
        return False
    
    async def _activate_search_fallback(self) -> bool:
        """Activate DuckDuckGo search fallback."""
        try:
            # Test if DDG is available
            try:
                from ddgs import DDGS
            except ImportError:
                from duckduckgo_search import DDGS
            
            with DDGS() as ddgs:
                results = list(ddgs.text("test", max_results=1))
                return len(results) > 0
        except Exception:
            return False
    
    async def _activate_wikipedia_fallback(self) -> bool:
        """Activate Wikipedia API fallback."""
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://en.wikipedia.org/api/rest_v1/page/summary/Test",
                    timeout=5
                ) as resp:
                    return resp.status == 200
        except Exception:
            return False
    
    async def _activate_api_fallback(self) -> bool:
        """Activate alternative API endpoint."""
        try:
            import aiohttp
            # Try alternative endpoint
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://generativelanguage.googleapis.com",
                    timeout=5
                ) as resp:
                    return resp.status < 500
        except Exception:
            return False
    
    async def _activate_dns_fallback(self) -> bool:
        """Activate fallback DNS."""
        try:
            import socket
            # Test if we can resolve with current DNS
            socket.gethostbyname("google.com")
            return True
        except Exception:
            return False
    
    def get_active_fallback(self, fallback_id: str) -> Optional[Dict]:
        """Get the currently active fallback for a service."""
        return self.active_fallbacks.get(fallback_id)
    
    def deactivate(self, fallback_id: str):
        """Deactivate a fallback."""
        if fallback_id in self.active_fallbacks:
            del self.active_fallbacks[fallback_id]
    
    def _setup_fallback_chains(self) -> Dict:
        """Setup fallback chains for various services."""
        return {
            "search_fallback": [
                {"type": "search_fallback", "name": "DuckDuckGo"},
                {"type": "wikipedia_fallback", "name": "Wikipedia API"},
            ],
            "wikipedia_fallback": [
                {"type": "wikipedia_fallback", "name": "Wikipedia API"},
            ],
            "api_endpoint": [
                {"type": "api_endpoint", "name": "Primary Gemini API"},
                {"type": "api_endpoint", "name": "Alternative endpoint"},
            ],
            "dns_fallback": [
                {"type": "dns_fallback", "name": "System DNS"},
                {"type": "dns_fallback", "name": "Google DNS (8.8.8.8)"},
            ],
        }
    
    def get_status(self) -> Dict:
        """Get fallback system status."""
        return {
            "active_fallbacks": list(self.active_fallbacks.keys()),
            "available_chains": list(self.fallback_chains.keys())
        }
