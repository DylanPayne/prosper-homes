from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, Any
import json
import os

class DebugLevel(Enum):
    OFF = 0
    ERROR = 1
    INFO = 2
    DEBUG = 3
    TRACE = 4

@dataclass
class DebugConfig:
    # Global debug level
    level: DebugLevel = DebugLevel.INFO
    
    # Module-specific debug levels (override global)
    module_levels: Dict[str, DebugLevel] = None
    
    # Feature flags for specific debug output
    show_annual_costs: bool = True
    show_monthly_breakdown: bool = False
    show_hourly_data: bool = False
    show_weather_cache_hits: bool = True
    show_api_calls: bool = True
    
    def __post_init__(self):
        if self.module_levels is None:
            self.module_levels = {}

    def should_log(self, level: DebugLevel, module: str = None) -> bool:
        """Check if we should log at this level for this module"""
        target_level = self.module_levels.get(module, self.level)
        return level.value <= target_level.value

# Global debug configuration - set default levels here
DEBUG_CONFIG = DebugConfig(
    level=DebugLevel.DEBUG,  # Show detailed output by default
    module_levels={
        'weather': DebugLevel.DEBUG,  # Show API calls and cache operations
        'energy': DebugLevel.INFO,    # Show major calculations
        'costs': DebugLevel.INFO      # Show cost summaries
    }
)

def debug_print(msg: str, level: DebugLevel = DebugLevel.INFO, module: str = None) -> None:
    """Print debug message if appropriate level is enabled"""
    if DEBUG_CONFIG.should_log(level, module):
        prefix = f"[{level.name}]"
        if module:
            prefix += f"[{module}]"
        print(f"{prefix} {msg}")

def debug_json(data: Any, level: DebugLevel = DebugLevel.DEBUG, module: str = None) -> None:
    """Print debug data as formatted JSON if appropriate level is enabled"""
    if DEBUG_CONFIG.should_log(level, module):
        prefix = f"[{level.name}]"
        if module:
            prefix += f"[{module}]"
        print(f"{prefix} {json.dumps(data, indent=2)}")

# Example usage:
if __name__ == "__main__":
    # Example debug messages
    debug_print("Starting application", DebugLevel.INFO)
    debug_print("Weather API call", DebugLevel.DEBUG, "weather")
    debug_print("Cache hit for ZIP 84101", DebugLevel.TRACE, "weather")
    
    # Example JSON debug
    debug_json({
        "annual_costs": {
            "electricity": 1200,
            "gas": 800
        }
    }, DebugLevel.INFO, "costs")
