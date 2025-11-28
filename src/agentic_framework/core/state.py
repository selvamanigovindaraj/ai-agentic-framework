from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class State:
    """Simple state holder for agents/workflows."""

    data: Dict[str, Any] = field(default_factory=dict)

    def update(self, updates: Dict[str, Any]) -> None:
        self.data.update(updates)

    def to_dict(self) -> Dict[str, Any]:
        return dict(self.data)
