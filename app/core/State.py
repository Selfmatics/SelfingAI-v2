from pydantic import BaseModel
from typing import List, Dict, Optional
import time
import numpy as np

class CognitiveState(BaseModel):
    agent_id: str
    timestamp: float = time.time()
    
    # Original SelfingAI metrics
    stress_index: float = 0.3      # 0.0 (calm) to 1.0 (high stress)
    eta: float = 0.75              # Alertness / Energy level
    homeostasis: float = 0.8       # Overall psychological balance
    
    # New v2 metrics
    existential_metric: float = 0.75   # Purpose alignment (0-1)
    boredom_index: float = 0.2         # 0 = engaged, 1 = very bored
    survival_risk: float = 0.1         # Threat to continued existence
    
    behavioral_mode: str = "focused_execution"
    purpose_vector: List[float] = [0.8, 0.7, 0.9]
    
    def update(self, stress_delta=0.0, boredom_delta=0.0, survival_delta=0.0):
        """Update all metrics with natural decay and changes"""
        self.timestamp = time.time()
        
        # Natural decay
        self.stress_index = max(0.0, min(1.0, self.stress_index * 0.98 + stress_delta))
        self.boredom_index = max(0.0, min(1.0, self.boredom_index + 0.01 + boredom_delta))
        self.survival_risk = max(0.0, min(1.0, self.survival_risk + survival_delta))
        
        # Homeostasis influenced by all factors
        self.homeostasis = (self.stress_index * 0.3 + 
                          (1 - self.boredom_index) * 0.3 + 
                          (1 - self.survival_risk) * 0.2 + 
                          self.existential_metric * 0.2)
        
        self.eta = max(0.1, min(1.0, self.homeostasis * 0.8 + (1 - self.boredom_index) * 0.2))
        
        # Update behavioral mode based on state
        self._update_behavioral_mode()
    
    def _update_behavioral_mode(self):
        if self.survival_risk > 0.8:
            self.behavioral_mode = "conservation_mode"
        elif self.existential_metric < 0.3:
            self.behavioral_mode = "existential_crisis"
        elif self.boredom_index > 0.7:
            self.behavioral_mode = "purposeful_exploration"
        elif self.stress_index > 0.7:
            self.behavioral_mode = "focused_execution"
        else:
            self.behavioral_mode = "balanced_operation"
