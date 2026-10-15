"""
core - Self-Healing System for Mark XLVIII

FBI/CIA-level autonomous debugging and self-repair system.
"""

from .healer import SelfHealer
from .detector import AnomalyDetector
from .researcher import SolutionResearcher
from .validator import FixValidator
from .fallback import FallbackManager
from .logger import DebugLogger

__all__ = [
    'SelfHealer',
    'AnomalyDetector',
    'SolutionResearcher',
    'FixValidator',
    'FallbackManager',
    'DebugLogger',
]

__version__ = "2.2.0"
__author__ = "Mark XLVIII Core Team"
