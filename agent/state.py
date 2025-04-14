# Purpose: Define and manage the state passed through LangGraph

from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class AgentState:
    preferences: Dict[str, Any] = field(default_factory=dict)
    destinations: List[Dict[str, Any]] = field(default_factory=list)
    itinerary: Dict[str, Any] = field(default_factory=dict)
    history: List[Dict[str, str]] = field(default_factory=list)
    is_followup: bool = False
    followup_response: str = ""

    def add_to_history(self, role: str, message: str):
        self.history.append({"role": role, "message": message})

