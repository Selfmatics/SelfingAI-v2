import numpy as np
from typing import List

class ExistentialModule:
    """
    Existential Metric - Measures how aligned the agent's actions are with its core purpose.
    """
    
    def __init__(self, purpose_vector: List[float] = None):
        # Default purpose: Help users effectively with empathy and accuracy
        self.purpose_vector = np.array(purpose_vector or [0.85, 0.75, 0.9])
        self.existential_metric: float = 0.75
        self.memory_actions: List[str] = []  # Simple memory of recent actions
    
    def update_purpose(self, new_purpose_vector: List[float]):
        """Change the agent's life purpose"""
        self.purpose_vector = np.array(new_purpose_vector)
    
    def add_action(self, action_description: str, impact_score: float = 0.5):
        """Record an action and update existential metric"""
        self.memory_actions.append(action_description)
        if len(self.memory_actions) > 20:  # Keep memory manageable
            self.memory_actions.pop(0)
        
        # Calculate coherence with purpose
        self._recalculate_existential_metric(impact_score)
    
    def _recalculate_existential_metric(self, impact_score: float):
        """Core calculation: Purpose coherence"""
        if not self.memory_actions:
            return
        
        # Simple coherence: higher impact and relevance = higher metric
        recent_impact = sum([impact_score] * min(5, len(self.memory_actions))) / 5
        coherence = min(1.0, recent_impact * 0.8 + 0.2)
        
        # Slow natural decay if no meaningful actions
        decay = 0.02 if len(self.memory_actions) < 3 else 0.005
        self.existential_metric = max(0.1, min(1.0, self.existential_metric * (1 - decay) + coherence * 0.1))
    
    def get_existential_metric(self) -> float:
        return round(self.existential_metric, 3)
    
    def is_in_crisis(self) -> bool:
        return self.existential_metric < 0.35
