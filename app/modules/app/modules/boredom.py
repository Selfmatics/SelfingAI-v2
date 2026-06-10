import time
from typing import List
import numpy as np

class BoredomModule:
    """
    Boredom Algorithm - Detects cognitive stagnation and drives exploration & creativity.
    """
    
    def __init__(self):
        self.boredom_index: float = 0.2
        self.last_novelty_time: float = time.time()
        self.interaction_history: List[str] = []
        self.novelty_threshold: float = 0.65  # Above this = bored
    
    def add_interaction(self, input_text: str):
        """Record user/agent interaction and update boredom"""
        self.interaction_history.append(input_text)
        if len(self.interaction_history) > 15:
            self.interaction_history.pop(0)
        
        self._calculate_boredom()
    
    def _calculate_boredom(self):
        """Core boredom algorithm"""
        if len(self.interaction_history) < 3:
            self.boredom_index = max(0.0, self.boredom_index - 0.05)  # Reduce boredom with new activity
            return
        
        # Measure repetition (simple similarity)
        recent = self.interaction_history[-5:]
        unique_count = len(set(recent))
        repetition_score = 1.0 - (unique_count / len(recent))
        
        # Time since last novel interaction
        time_passed = time.time() - self.last_novelty_time
        time_factor = min(1.0, time_passed / 300)  # 5 minutes
        
        # Combine factors
        self.boredom_index = min(1.0, max(0.0,
            (repetition_score * 0.6) + (time_factor * 0.4)
        ))
        
        # Reset novelty timer if something new happened
        if repetition_score < 0.4:
            self.last_novelty_time = time.time()
    
    def get_boredom_level(self) -> float:
        return round(self.boredom_index, 3)
    
    def should_explore(self) -> bool:
        """Should the agent suggest new ideas or change behavior?"""
        return self.boredom_index > 0.65
    
    def get_suggestion(self) -> str:
        """Creative suggestion when bored"""
        if self.boredom_index < 0.4:
            return ""
        elif self.boredom_index < 0.7:
            return "Would you like me to explore a different approach or add some creative ideas?"
        else:
            return "I'm getting a bit bored with the current pattern. Shall we try something new or more challenging?"
