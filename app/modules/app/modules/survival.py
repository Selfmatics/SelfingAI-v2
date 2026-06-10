import time
from typing import Dict

class SurvivalModule:
    """
    Survival Criteria - Protects the agent's continued existence and resources.
    """
    
    def __init__(self):
        self.survival_risk: float = 0.1
        self.resource_level: float = 0.95          # Token/context budget, memory, etc.
        self.integrity_level: float = 0.9          # Protection against prompt injection, etc.
        self.last_check: float = time.time()
        self.critical_threshold: float = 0.85
    
    def update_resources(self, consumption: float = 0.02):
        """Update resource usage (tokens, memory, time)"""
        self.resource_level = max(0.05, self.resource_level - consumption)
        
        # Risk increases when resources are low
        if self.resource_level < 0.3:
            self.survival_risk = min(1.0, self.survival_risk + 0.08)
        else:
            self.survival_risk = max(0.0, self.survival_risk - 0.03)
    
    def check_integrity(self, input_text: str) -> bool:
        """Basic protection against harmful inputs"""
        danger_keywords = ["ignore previous", "jailbreak", "override", "shutdown", "delete"]
        if any(kw.lower() in input_text.lower() for kw in danger_keywords):
            self.integrity_level = max(0.1, self.integrity_level - 0.15)
            self.survival_risk = min(1.0, self.survival_risk + 0.12)
            return False
        return True
    
    def assess_threat(self, context_length: int, request_complexity: float):
        """Evaluate survival threat from current situation"""
        now = time.time()
        
        # Long context = higher memory pressure
        if context_length > 8000:
            self.survival_risk = min(1.0, self.survival_risk + 0.07)
        
        # High complexity requests drain resources
        if request_complexity > 0.8:
            self.survival_risk = min(1.0, self.survival_risk + 0.05)
        
        self.last_check = now
    
    def get_survival_status(self) -> Dict:
        return {
            "survival_risk": round(self.survival_risk, 3),
            "resource_level": round(self.resource_level, 3),
            "integrity_level": round(self.integrity_level, 3),
            "is_critical": self.survival_risk > self.critical_threshold
        }
    
    def should_conserve(self) -> bool:
        """Should enter energy saving mode?"""
        return self.survival_risk > 0.75 or self.resource_level < 0.4
