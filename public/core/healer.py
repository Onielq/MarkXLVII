"""
core/healer.py - Main Self-Repair Orchestrator

FBI/CIA-level autonomous debugging system.
Coordinates detection, analysis, research, and repair operations.
"""

import asyncio
import time
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

from .detector import AnomalyDetector
from .researcher import SolutionResearcher
from .validator import FixValidator
from .fallback import FallbackManager
from .logger import DebugLogger


class SelfHealer:
    """
    Main self-healing orchestrator.
    Monitors system health and autonomously repairs issues.
    """
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.detector = AnomalyDetector()
        self.researcher = SolutionResearcher(base_dir)
        self.validator = FixValidator()
        self.fallback = FallbackManager(base_dir)
        self.logger = DebugLogger(base_dir / "logs" / "healing_sessions.log")
        
        self.is_monitoring = False
        self.active_sessions: Dict[str, Dict] = {}
        self.healing_history = []
        
        # Performance tracking
        self.total_heals = 0
        self.successful_heals = 0
        self.avg_recovery_time = 0.0
        
    async def start_monitoring(self):
        """Start continuous health monitoring."""
        self.is_monitoring = True
        self.logger.log("INFO", "Self-healing system started")
        
        while self.is_monitoring:
            try:
                # Check for anomalies
                anomalies = await self.detector.scan()
                
                for anomaly in anomalies:
                    session_id = f"heal_{int(time.time())}_{anomaly['type']}"
                    await self._handle_anomaly(session_id, anomaly)
                
                # Monitor every 2 seconds
                await asyncio.sleep(2)
                
            except Exception as e:
                self.logger.log("ERROR", f"Monitoring error: {e}")
                await asyncio.sleep(5)
    
    async def stop_monitoring(self):
        """Stop health monitoring."""
        self.is_monitoring = False
        self.logger.log("INFO", "Self-healing system stopped")
    
    async def _handle_anomaly(self, session_id: str, anomaly: Dict):
        """Handle a detected anomaly through the healing pipeline."""
        start_time = time.time()
        
        self.logger.log("INFO", f"[{session_id}] Anomaly detected: {anomaly['type']}")
        
        # Initialize session
        self.active_sessions[session_id] = {
            "anomaly": anomaly,
            "start_time": start_time,
            "status": "analyzing",
            "steps": []
        }
        
        try:
            # Phase 1: Analyze
            analysis = await self._analyze(anomaly)
            self._log_step(session_id, "analyze", analysis)
            
            # Phase 2: Research solutions
            self.active_sessions[session_id]["status"] = "researching"
            solutions = await self.researcher.find_solutions(anomaly, analysis)
            self._log_step(session_id, "research", {"solutions": len(solutions)})
            
            # Phase 3: Test and apply fixes
            self.active_sessions[session_id]["status"] = "testing"
            fix_applied = False
            
            for solution in solutions:
                # Test in isolation
                test_result = await self.validator.test_fix(solution)
                
                if test_result["success"]:
                    # Apply the fix
                    self.active_sessions[session_id]["status"] = "fixing"
                    await self._apply_fix(solution)
                    fix_applied = True
                    self._log_step(session_id, "fix", solution)
                    break
            
            # Phase 4: Verify
            self.active_sessions[session_id]["status"] = "verifying"
            verification = await self.validator.verify_fix(anomaly)
            self._log_step(session_id, "verify", verification)
            
            # Complete session
            recovery_time = time.time() - start_time
            
            if verification["success"]:
                self.active_sessions[session_id]["status"] = "complete"
                self.successful_heals += 1
                self.logger.log("SUCCESS", f"[{session_id}] Issue resolved in {recovery_time:.2f}s")
            else:
                self.active_sessions[session_id]["status"] = "failed"
                self.logger.log("WARNING", f"[{session_id}] Fix verification failed")
            
            # Update statistics
            self.total_heals += 1
            self.avg_recovery_time = (
                (self.avg_recovery_time * (self.total_heals - 1) + recovery_time) 
                / self.total_heals
            )
            
        except Exception as e:
            self.active_sessions[session_id]["status"] = "error"
            self.logger.log("ERROR", f"[{session_id}] Healing error: {e}")
        
        # Archive session
        self.healing_history.append(self.active_sessions[session_id])
        del self.active_sessions[session_id]
    
    async def _analyze(self, anomaly: Dict) -> Dict:
        """Analyze the anomaly to determine root cause."""
        return {
            "root_cause": anomaly.get("details", "Unknown"),
            "severity": anomaly.get("severity", "medium"),
            "impact": anomaly.get("impact", "unknown"),
            "category": anomaly["type"]
        }
    
    async def _apply_fix(self, solution: Dict):
        """Apply a fix solution."""
        fix_type = solution.get("type")
        
        if fix_type == "install_dependency":
            await self._install_dependency(solution["package"])
        elif fix_type == "restore_backup":
            await self._restore_backup(solution["backup_path"])
        elif fix_type == "reconnect":
            await self._reconnect_service(solution["service"])
        elif fix_type == "regenerate_config":
            await self._regenerate_config(solution["config_path"])
        elif fix_type == "fallback":
            await self.fallback.activate(solution["fallback_id"])
    
    async def _install_dependency(self, package: str):
        """Install a missing Python package."""
        import subprocess
        self.logger.log("INFO", f"Installing package: {package}")
        
        proc = await asyncio.create_subprocess_exec(
            "pip", "install", package, "--quiet",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await proc.communicate()
    
    async def _restore_backup(self, backup_path: str):
        """Restore from a backup file."""
        import shutil
        self.logger.log("INFO", f"Restoring backup: {backup_path}")
        
        source = Path(backup_path)
        if source.exists():
            # Determine target based on backup name
            target_name = source.stem.replace("_backup", "")
            target = self.base_dir / source.parent.name / target_name
            shutil.copy2(source, target)
    
    async def _reconnect_service(self, service: str):
        """Reconnect to a service."""
        self.logger.log("INFO", f"Reconnecting service: {service}")
        # Service-specific reconnection logic would go here
    
    async def _regenerate_config(self, config_path: str):
        """Regenerate a configuration file."""
        self.logger.log("INFO", f"Regenerating config: {config_path}")
        # Config regeneration logic would go here
    
    def _log_step(self, session_id: str, phase: str, data: Dict):
        """Log a healing step."""
        self.active_sessions[session_id]["steps"].append({
            "phase": phase,
            "timestamp": time.time(),
            "data": data
        })
    
    def get_status(self) -> Dict:
        """Get current healing system status."""
        return {
            "monitoring": self.is_monitoring,
            "active_sessions": len(self.active_sessions),
            "total_heals": self.total_heals,
            "successful_heals": self.successful_heals,
            "success_rate": (
                (self.successful_heals / self.total_heals * 100) 
                if self.total_heals > 0 else 0
            ),
            "avg_recovery_time": self.avg_recovery_time,
            "recent_sessions": self.healing_history[-5:]
        }
