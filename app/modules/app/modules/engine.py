import time
from typing import Dict, Any
from .state import CognitiveState
from ..modules.existential import ExistentialModule
from ..modules.boredom import BoredomModule
from ..modules.survival import SurvivalModule

class SelfingEngine:
    """
    Main Cognitive Organism Engine for SelfingAI-v2
    Combines all modules into a living cognitive system.
    """
    
    def __init__(self, agent_id: str = "default_agent"):
        self.state = CognitiveState(agent_id=agent_id)
        
        # Initialize modules
        self.existential = ExistentialModule()
        self.boredom = BoredomModule()
        self.survival = SurvivalModule()
        
        self.last_update = time.time()
    
    def process_input(self, user_input: str, context_length: int = 0, complexity: float = 0.5) -> Dict[str, Any]:
        """Main entry point: Process input and return updated state + behavior suggestions"""
        
        # Update survival first
        self.survival.check_integrity(user_input)
        self.survival.update_resources(consumption=0.015)
        self.survival.assess_threat(context_length, complexity)
        
        # Update boredom
        self.boredom.add_interaction(user_input)
        
        # Record action for existential
        self.existential.add_action(user_input, impact_score=0.6)
        
        # Update main cognitive state
        stress_delta = 0.08 if len(user_input) > 200 else 0.0
        boredom_delta = self.boredom.get_boredom_level() * 0.1
        survival_delta = self.survival.survival_risk * 0.05
        
        self.state.update(
            stress_delta=stress_delta,
            boredom_delta=boredom_delta,
            survival_delta=survival_delta
        )
        
        # Sync existential metric
        self.state.existential_metric = self.existential.get_existential_metric()
        
        self.last_update = time.time()
        
        return self.get_full_state()
    
    def get_full_state(self) -> Dict[str, Any]:
        """Return complete cognitive state"""
        return {
            "agent_id": self.state.agent_id,
            "timestamp": self.state.timestamp,
            "stress_index": round(self.state.stress_index, 3),
            "eta": round(self.state.eta, 3),
            "homeostasis": round(self.state.homeostasis, 3),
            "existential_metric": round(self.state.existential_metric, 3),
            "boredom_index": round(self.state.boredom_index, 3),
            "survival_risk": round(self.state.survival_risk, 3),
            "behavioral_mode": self.state.behavioral_mode,
            "survival_status": self.survival.get_survival_status(),
            "boredom_suggestion": self.boredom.get_suggestion(),
            "is_existential_crisis": self.existential.is_in_crisis()
        }
    
    def get_response_modifier(self) -> Dict[str, str]:
        """Suggestions for how the LLM should respond based on internal state"""
        modifiers = {}
        
        if self.state.behavioral_mode == "conservation_mode":
            modifiers["style"] = "short, efficient, and resource-saving"
        elif self.state.behavioral_mode == "purposeful_exploration":
            modifiers["style"] = "creative and exploratory"
        elif self.state.behavioral_mode == "existential_crisis":
            modifiers["style"] = "thoughtful and seeking purpose clarification"
        
        if self.boredom.should_explore():
            modifiers["add"] = "include fresh ideas or alternative approaches"
        
        return modifiers
