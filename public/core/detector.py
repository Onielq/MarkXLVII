"""
core/detector.py - Anomaly Detection Engine

Real-time anomaly detection and error pattern recognition.
Monitors all system components for issues.
"""

import asyncio
import re
import time
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


class AnomalyDetector:
    """
    Detects anomalies across all system components.
    Uses pattern recognition and health checks.
    """
    
    def __init__(self):
        self.error_patterns = self._load_error_patterns()
        self.health_checks = self._setup_health_checks()
        self.recent_errors = []
        self.max_history = 100
    
    async def scan(self) -> List[Dict]:
        """Scan all systems for anomalies."""
        anomalies = []
        
        # Check error logs
        log_anomalies = await self._check_error_logs()
        anomalies.extend(log_anomalies)
        
        # Check system health
        health_anomalies = await self._check_system_health()
        anomalies.extend(health_anomalies)
        
        # Check memory integrity
        memory_anomalies = await self._check_memory_integrity()
        anomalies.extend(memory_anomalies)
        
        # Check network connectivity
        network_anomalies = await self._check_network()
        anomalies.extend(network_anomalies)
        
        return anomalies
    
    async def _check_error_logs(self) -> List[Dict]:
        """Check recent error logs for patterns."""
        anomalies = []
        
        # Check if there are recent errors in memory
        # This would integrate with the actual error logging system
        try:
            # Simulate checking logs - in real implementation, 
            # this would read from actual log files
            if len(self.recent_errors) > 0:
                for error in self.recent_errors[-10:]:
                    pattern = self._match_error_pattern(error)
                    if pattern:
                        anomalies.append({
                            "type": pattern["category"],
                            "severity": pattern["severity"],
                            "details": error,
                            "pattern": pattern["name"],
                            "timestamp": time.time()
                        })
        except Exception:
            pass
        
        return anomalies
    
    async def _check_system_health(self) -> List[Dict]:
        """Check overall system health."""
        anomalies = []
        
        # Check CPU usage
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=0.1)
            if cpu_percent > 90:
                anomalies.append({
                    "type": "performance",
                    "severity": "high",
                    "details": f"CPU usage at {cpu_percent}%",
                    "metric": "cpu",
                    "value": cpu_percent
                })
        except ImportError:
            pass
        
        # Check memory usage
        try:
            import psutil
            memory = psutil.virtual_memory()
            if memory.percent > 90:
                anomalies.append({
                    "type": "performance",
                    "severity": "high",
                    "details": f"Memory usage at {memory.percent}%",
                    "metric": "memory",
                    "value": memory.percent
                })
        except ImportError:
            pass
        
        return anomalies
    
    async def _check_memory_integrity(self) -> List[Dict]:
        """Check memory file integrity."""
        anomalies = []
        
        memory_file = Path("memory/memory.json")
        if memory_file.exists():
            try:
                import json
                with open(memory_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Try to parse JSON
                    json.loads(content)
            except json.JSONDecodeError as e:
                anomalies.append({
                    "type": "memory_corruption",
                    "severity": "critical",
                    "details": f"Memory file corrupted: {str(e)}",
                    "file": str(memory_file)
                })
            except UnicodeDecodeError as e:
                anomalies.append({
                    "type": "memory_corruption",
                    "severity": "critical",
                    "details": f"Memory file encoding error: {str(e)}",
                    "file": str(memory_file)
                })
        
        return anomalies
    
    async def _check_network(self) -> List[Dict]:
        """Check network connectivity."""
        anomalies = []
        
        # Check if we can reach common endpoints
        endpoints = [
            ("Google", "https://www.google.com"),
            ("Gemini API", "https://generativelanguage.googleapis.com"),
        ]
        
        for name, url in endpoints:
            try:
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                        if resp.status >= 500:
                            anomalies.append({
                                "type": "network",
                                "severity": "medium",
                                "details": f"{name} returned status {resp.status}",
                                "endpoint": url
                            })
            except Exception as e:
                anomalies.append({
                    "type": "network",
                    "severity": "high",
                    "details": f"Cannot reach {name}: {str(e)}",
                    "endpoint": url
                })
        
        return anomalies
    
    def _match_error_pattern(self, error: str) -> Dict:
        """Match error string against known patterns."""
        error_lower = error.lower()
        
        for pattern_name, pattern_data in self.error_patterns.items():
            for keyword in pattern_data["keywords"]:
                if keyword in error_lower:
                    return {
                        "name": pattern_name,
                        "category": pattern_data["category"],
                        "severity": pattern_data["severity"]
                    }
        
        return None
    
    def _load_error_patterns(self) -> Dict:
        """Load known error patterns."""
        return {
            "api_quota": {
                "keywords": ["quota", "rate limit", "429", "too many requests"],
                "category": "api_error",
                "severity": "medium"
            },
            "network_timeout": {
                "keywords": ["timeout", "connection refused", "network unreachable"],
                "category": "network",
                "severity": "high"
            },
            "missing_dependency": {
                "keywords": ["modulenotfounderror", "no module named", "importerror"],
                "category": "dependency",
                "severity": "medium"
            },
            "file_not_found": {
                "keywords": ["filenotfounderror", "no such file", "file not found"],
                "category": "file_system",
                "severity": "medium"
            },
            "memory_corruption": {
                "keywords": ["jsondecodeerror", "unicodedecodeerror", "corrupted"],
                "category": "memory",
                "severity": "critical"
            },
            "permission_denied": {
                "keywords": ["permissiondenied", "access denied", "permission error"],
                "category": "permissions",
                "severity": "medium"
            }
        }
    
    def _setup_health_checks(self) -> List[Dict]:
        """Setup health check configurations."""
        return [
            {"name": "cpu", "threshold": 90, "unit": "percent"},
            {"name": "memory", "threshold": 90, "unit": "percent"},
            {"name": "disk", "threshold": 95, "unit": "percent"},
        ]
    
    def record_error(self, error: str):
        """Record an error for pattern analysis."""
        self.recent_errors.append({
            "error": error,
            "timestamp": time.time()
        })
        
        # Keep only recent history
        if len(self.recent_errors) > self.max_history:
            self.recent_errors = self.recent_errors[-self.max_history:]
    
    def get_stats(self) -> Dict:
        """Get detection statistics."""
        return {
            "recent_errors": len(self.recent_errors),
            "patterns_loaded": len(self.error_patterns),
            "health_checks": len(self.health_checks)
        }
