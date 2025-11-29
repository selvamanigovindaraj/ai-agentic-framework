import json
import os
from typing import Dict, Any, Optional

class ProceduralMemory:
    """
    Stores procedural knowledge (rules, preferences) as key-value pairs.
    Backed by a JSON file.
    """
    
    def __init__(self, filepath: str = "procedural_memory.json"):
        self.filepath = filepath
        self.memory: Dict[str, Any] = {}
        self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as f:
                    self.memory = json.load(f)
            except json.JSONDecodeError:
                self.memory = {}

    def _save(self):
        with open(self.filepath, "w") as f:
            json.dump(self.memory, f, indent=2)

    def set_preference(self, key: str, value: Any):
        """Set a preference or rule"""
        self.memory[key] = value
        self._save()

    def get_preference(self, key: str) -> Optional[Any]:
        """Get a preference"""
        return self.memory.get(key)

    def get_all_context(self) -> str:
        """Get all preferences formatted as context string"""
        if not self.memory:
            return ""
        
        context = "User Preferences / Rules:\n"
        for k, v in self.memory.items():
            context += f"- {k}: {v}\n"
        return context
