"""
core/logger.py - Debug Session Logging

Logs all healing sessions for analysis and pattern learning.
"""

import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List


class DebugLogger:
    """
    Logs all healing sessions and system events.
    Provides pattern analysis and historical data.
    """
    
    def __init__(self, log_path: Path):
        self.log_path = log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Ensure log file exists
        if not self.log_path.exists():
            self.log_path.write_text("")
    
    def log(self, level: str, message: str, data: Dict = None):
        """Log a message with timestamp and optional data."""
        timestamp = datetime.now().isoformat()
        
        entry = {
            "timestamp": timestamp,
            "level": level,
            "message": message,
        }
        
        if data:
            entry["data"] = data
        
        # Append to log file
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + "\n")
    
    def log_session(self, session: Dict):
        """Log a complete healing session."""
        self.log("SESSION", "Healing session completed", {
            "session_id": session.get("id"),
            "anomaly_type": session.get("anomaly", {}).get("type"),
            "status": session.get("status"),
            "steps": len(session.get("steps", [])),
            "recovery_time": session.get("recovery_time", 0)
        })
    
    def get_recent_logs(self, count: int = 50) -> List[Dict]:
        """Get recent log entries."""
        if not self.log_path.exists():
            return []
        
        try:
            with open(self.log_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Get last N lines
            recent = lines[-count:] if len(lines) > count else lines
            
            logs = []
            for line in recent:
                try:
                    logs.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue
            
            return logs
        except Exception:
            return []
    
    def get_sessions(self, count: int = 10) -> List[Dict]:
        """Get recent healing sessions."""
        logs = self.get_recent_logs(100)
        sessions = [log for log in logs if log.get("level") == "SESSION"]
        return sessions[-count:]
    
    def get_stats(self) -> Dict:
        """Get logging statistics."""
        logs = self.get_recent_logs(1000)
        
        level_counts = {}
        for log in logs:
            level = log.get("level", "UNKNOWN")
            level_counts[level] = level_counts.get(level, 0) + 1
        
        return {
            "total_logs": len(logs),
            "by_level": level_counts,
            "log_file_size": self.log_path.stat().st_size if self.log_path.exists() else 0
        }
    
    def clear_logs(self):
        """Clear all logs."""
        if self.log_path.exists():
            self.log_path.write_text("")
    
    def search_logs(self, query: str) -> List[Dict]:
        """Search logs for a specific query."""
        logs = self.get_recent_logs(10000)
        query_lower = query.lower()
        
        results = []
        for log in logs:
            if (query_lower in log.get("message", "").lower() or
                query_lower in json.dumps(log.get("data", {})).lower()):
                results.append(log)
        
        return results
    
    def analyze_patterns(self) -> Dict:
        """Analyze log patterns for recurring issues."""
        logs = self.get_recent_logs(1000)
        
        # Count error types
        error_patterns = {}
        for log in logs:
            if log.get("level") in ["ERROR", "WARNING"]:
                message = log.get("message", "")
                # Extract key pattern
                pattern = message[:50]  # Simple pattern extraction
                error_patterns[pattern] = error_patterns.get(pattern, 0) + 1
        
        # Sort by frequency
        sorted_patterns = sorted(
            error_patterns.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        return {
            "top_errors": sorted_patterns,
            "total_errors": sum(error_patterns.values()),
            "unique_patterns": len(error_patterns)
        }
