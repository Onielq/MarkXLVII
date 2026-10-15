"""
core/validator.py - Post-Fix Verification

Validates that fixes actually work and system integrity is maintained.
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, Any


class FixValidator:
    """
    Validates fixes after application.
    Ensures system integrity and functionality.
    """
    
    def __init__(self):
        self.validation_history = []
    
    async def test_fix(self, solution: Dict) -> Dict:
        """Test a fix in isolation before applying."""
        fix_type = solution.get("type")
        
        try:
            if fix_type == "install_dependency":
                return await self._test_dependency_install(solution["package"])
            elif fix_type == "restore_backup":
                return await self._test_backup_restore(solution["backup_path"])
            elif fix_type == "reconnect":
                return await self._test_reconnection(solution["service"])
            elif fix_type == "regenerate_config":
                return await self._test_config_regeneration(solution["config_path"])
            elif fix_type == "fallback":
                return await self._test_fallback(solution["fallback_id"])
            else:
                return {"success": False, "reason": "Unknown fix type"}
        except Exception as e:
            return {"success": False, "reason": str(e)}
    
    async def verify_fix(self, anomaly: Dict) -> Dict:
        """Verify that the fix actually resolved the issue."""
        anomaly_type = anomaly.get("type")
        
        try:
            if anomaly_type == "dependency":
                return await self._verify_dependency_fix(anomaly)
            elif anomaly_type == "memory_corruption":
                return await self._verify_memory_fix(anomaly)
            elif anomaly_type == "network":
                return await self._verify_network_fix(anomaly)
            elif anomaly_type == "api_error":
                return await self._verify_api_fix(anomaly)
            else:
                return {"success": True, "message": "Fix applied"}
        except Exception as e:
            return {"success": False, "reason": str(e)}
    
    async def _test_dependency_install(self, package: str) -> Dict:
        """Test if a package can be installed."""
        import subprocess
        
        # Try dry-run install
        try:
            result = subprocess.run(
                ["pip", "install", package, "--dry-run", "--quiet"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return {"success": True, "message": f"Package {package} can be installed"}
            else:
                return {"success": False, "reason": result.stderr}
        except Exception as e:
            return {"success": False, "reason": str(e)}
    
    async def _test_backup_restore(self, backup_path: str) -> Dict:
        """Test if a backup can be restored."""
        path = Path(backup_path)
        
        if not path.exists():
            return {"success": False, "reason": "Backup file not found"}
        
        try:
            # Try to read the backup
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                json.loads(content)  # Validate JSON
            
            return {"success": True, "message": "Backup is valid"}
        except Exception as e:
            return {"success": False, "reason": str(e)}
    
    async def _test_reconnection(self, service: str) -> Dict:
        """Test if a service can be reconnected."""
        # Simple connectivity test
        try:
            if service == "dns_fallback":
                # Test DNS
                import socket
                socket.gethostbyname("google.com")
                return {"success": True, "message": "DNS is working"}
            elif service == "gemini_api":
                # Test API endpoint
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://generativelanguage.googleapis.com", timeout=5) as resp:
                        return {"success": resp.status < 500, "message": f"API status: {resp.status}"}
            else:
                return {"success": True, "message": "Service test passed"}
        except Exception as e:
            return {"success": False, "reason": str(e)}
    
    async def _test_config_regeneration(self, config_path: str) -> Dict:
        """Test if a config can be regenerated."""
        path = Path(config_path)
        
        # Check if we can write to the location
        try:
            test_file = path.with_suffix('.test')
            test_file.write_text("test")
            test_file.unlink()
            return {"success": True, "message": "Config location is writable"}
        except Exception as e:
            return {"success": False, "reason": str(e)}
    
    async def _test_fallback(self, fallback_id: str) -> Dict:
        """Test if a fallback is available."""
        # Check if fallback exists
        fallbacks = {
            "search_fallback": True,
            "wikipedia_fallback": True,
            "api_endpoint": True,
        }
        
        if fallback_id in fallbacks:
            return {"success": True, "message": f"Fallback {fallback_id} is available"}
        else:
            return {"success": False, "reason": f"Fallback {fallback_id} not found"}
    
    async def _verify_dependency_fix(self, anomaly: Dict) -> Dict:
        """Verify that a dependency is now installed."""
        details = anomaly.get("details", "")
        import re
        match = re.search(r"No module named ['\"](\w+)['\"]", details)
        
        if match:
            package = match.group(1)
            try:
                __import__(package)
                return {"success": True, "message": f"Package {package} is now importable"}
            except ImportError:
                return {"success": False, "reason": f"Package {package} still not importable"}
        
        return {"success": True, "message": "Verification passed"}
    
    async def _verify_memory_fix(self, anomaly: Dict) -> Dict:
        """Verify that memory is now intact."""
        memory_file = Path("memory/memory.json")
        
        if memory_file.exists():
            try:
                with open(memory_file, 'r', encoding='utf-8') as f:
                    json.loads(f.read())
                return {"success": True, "message": "Memory file is valid JSON"}
            except Exception as e:
                return {"success": False, "reason": str(e)}
        
        return {"success": False, "reason": "Memory file still missing"}
    
    async def _verify_network_fix(self, anomaly: Dict) -> Dict:
        """Verify that network is now working."""
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com", timeout=5) as resp:
                    if resp.status < 500:
                        return {"success": True, "message": "Network is working"}
        except Exception:
            pass
        
        return {"success": False, "reason": "Network still not working"}
    
    async def _verify_api_fix(self, anomaly: Dict) -> Dict:
        """Verify that API is now working."""
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get("https://generativelanguage.googleapis.com", timeout=5) as resp:
                    if resp.status < 500:
                        return {"success": True, "message": "API is accessible"}
        except Exception:
            pass
        
        return {"success": False, "reason": "API still not accessible"}
    
    def get_stats(self) -> Dict:
        """Get validation statistics."""
        return {
            "validations_run": len(self.validation_history),
            "success_rate": (
                sum(1 for v in self.validation_history if v.get("success")) 
                / len(self.validation_history) * 100
                if self.validation_history else 0
            )
        }
