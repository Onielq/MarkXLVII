"""
core/researcher.py - Autonomous Solution Research

Finds solutions through web search, documentation, and code analysis.
"""

import asyncio
import json
from pathlib import Path
from typing import List, Dict, Any


class SolutionResearcher:
    """
    Autonomously researches solutions for detected issues.
    Uses multiple sources: web, docs, code patterns.
    """
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.solution_cache = {}
        self.max_cache_size = 1000
    
    async def find_solutions(self, anomaly: Dict, analysis: Dict) -> List[Dict]:
        """Find potential solutions for an anomaly."""
        solutions = []
        
        anomaly_type = anomaly.get("type", "unknown")
        
        # Try cached solutions first
        cache_key = f"{anomaly_type}:{analysis.get('root_cause', '')}"
        if cache_key in self.solution_cache:
            return self.solution_cache[cache_key]
        
        # Research based on anomaly type
        if anomaly_type == "dependency":
            solutions = await self._research_dependency_fix(anomaly)
        elif anomaly_type == "memory_corruption":
            solutions = await self._research_memory_fix(anomaly)
        elif anomaly_type == "network":
            solutions = await self._research_network_fix(anomaly)
        elif anomaly_type == "api_error":
            solutions = await self._research_api_fix(anomaly)
        elif anomaly_type == "file_system":
            solutions = await self._research_file_fix(anomaly)
        else:
            solutions = await self._research_generic_fix(anomaly, analysis)
        
        # Cache the solutions
        if len(self.solution_cache) < self.max_cache_size:
            self.solution_cache[cache_key] = solutions
        
        return solutions
    
    async def _research_dependency_fix(self, anomaly: Dict) -> List[Dict]:
        """Research solutions for missing dependencies."""
        solutions = []
        details = anomaly.get("details", "")
        
        # Extract package name from error
        import re
        match = re.search(r"No module named ['\"](\w+)['\"]", details)
        if match:
            package = match.group(1)
            solutions.append({
                "type": "install_dependency",
                "package": package,
                "confidence": 0.95,
                "description": f"Install missing package: {package}"
            })
        
        # Try to find alternative packages
        alternatives = self._get_package_alternatives(package if match else "")
        for alt in alternatives:
            solutions.append({
                "type": "install_dependency",
                "package": alt,
                "confidence": 0.7,
                "description": f"Try alternative package: {alt}"
            })
        
        return solutions
    
    async def _research_memory_fix(self, anomaly: Dict) -> List[Dict]:
        """Research solutions for memory corruption."""
        solutions = []
        
        # Look for backup files
        backup_dir = self.base_dir / "memory" / "backup"
        if backup_dir.exists():
            backups = list(backup_dir.glob("*.json"))
            if backups:
                latest = max(backups, key=lambda p: p.stat().st_mtime)
                solutions.append({
                    "type": "restore_backup",
                    "backup_path": str(latest),
                    "confidence": 0.9,
                    "description": f"Restore from backup: {latest.name}"
                })
        
        # Try to regenerate memory file
        solutions.append({
            "type": "regenerate_config",
            "config_path": str(self.base_dir / "memory" / "memory.json"),
            "confidence": 0.6,
            "description": "Regenerate memory file from scratch"
        })
        
        return solutions
    
    async def _research_network_fix(self, anomaly: Dict) -> List[Dict]:
        """Research solutions for network issues."""
        solutions = []
        
        # Try DNS fallback
        solutions.append({
            "type": "reconnect",
            "service": "dns_fallback",
            "confidence": 0.8,
            "description": "Switch to fallback DNS (8.8.8.8)"
        })
        
        # Try alternative endpoints
        solutions.append({
            "type": "fallback",
            "fallback_id": "api_endpoint",
            "confidence": 0.7,
            "description": "Switch to alternative API endpoint"
        })
        
        # Wait and retry
        solutions.append({
            "type": "retry",
            "delay": 5,
            "confidence": 0.5,
            "description": "Wait 5 seconds and retry connection"
        })
        
        return solutions
    
    async def _research_api_fix(self, anomaly: Dict) -> List[Dict]:
        """Research solutions for API errors."""
        solutions = []
        details = anomaly.get("details", "")
        
        # Check if it's a quota issue
        if "quota" in details.lower() or "429" in details:
            # Try fallback search
            solutions.append({
                "type": "fallback",
                "fallback_id": "search_fallback",
                "confidence": 0.9,
                "description": "Switch to DuckDuckGo search fallback"
            })
            
            # Try Wikipedia
            solutions.append({
                "type": "fallback",
                "fallback_id": "wikipedia_fallback",
                "confidence": 0.8,
                "description": "Switch to Wikipedia API fallback"
            })
        
        # Try reconnection
        solutions.append({
            "type": "reconnect",
            "service": "gemini_api",
            "confidence": 0.7,
            "description": "Reconnect to Gemini API"
        })
        
        return solutions
    
    async def _research_file_fix(self, anomaly: Dict) -> List[Dict]:
        """Research solutions for file system issues."""
        solutions = []
        details = anomaly.get("details", "")
        
        # Try to find the file in common locations
        import re
        match = re.search(r"['\"]([^'\"]+)['\"]", details)
        if match:
            missing_file = match.group(1)
            
            # Check common locations
            common_paths = [
                self.base_dir / missing_file,
                Path.home() / missing_file,
                Path.cwd() / missing_file,
            ]
            
            for path in common_paths:
                if path.exists():
                    solutions.append({
                        "type": "update_path",
                        "old_path": missing_file,
                        "new_path": str(path),
                        "confidence": 0.8,
                        "description": f"Found file at: {path}"
                    })
        
        return solutions
    
    async def _research_generic_fix(self, anomaly: Dict, analysis: Dict) -> List[Dict]:
        """Research generic solutions."""
        solutions = []
        
        # Try web search for solution
        query = f"{anomaly.get('type')} {analysis.get('root_cause', '')} solution"
        
        # For now, return generic solutions
        solutions.append({
            "type": "restart_service",
            "service": "main",
            "confidence": 0.4,
            "description": "Restart the main service"
        })
        
        solutions.append({
            "type": "clear_cache",
            "confidence": 0.3,
            "description": "Clear application cache"
        })
        
        return solutions
    
    def _get_package_alternatives(self, package: str) -> List[str]:
        """Get alternative packages for common imports."""
        alternatives_map = {
            "duckduckgo_search": ["ddgs"],
            "ddgs": ["duckduckgo_search"],
            "PIL": ["Pillow"],
            "cv2": ["opencv-python"],
            "sklearn": ["scikit-learn"],
        }
        
        return alternatives_map.get(package, [])
    
    def get_stats(self) -> Dict:
        """Get research statistics."""
        return {
            "cached_solutions": len(self.solution_cache),
            "max_cache_size": self.max_cache_size
        }
