"""Base Tool class and schema"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import uuid


@dataclass
class ToolSchema:
    """Tool input/output schema"""
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    
    def validate_input(self, params: Dict[str, Any]) -> bool:
        """Validate input parameters"""
        # JSON Schema validation would go here
        return True
    
    def validate_output(self, result: Any) -> bool:
        """Validate output"""
        return True


@dataclass
class Tool(ABC):
    """Base Tool class with standardized interface"""
    
    id: str = field(default_factory=lambda: f"tool_{uuid.uuid4().hex[:8]}")
    name: str = ""
    description: str = ""
    category: str = "general"
    version: str = "1.0.0"
    schema: Optional[ToolSchema] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        """Execute the tool"""
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "version": self.version,
            "metadata": self.metadata
        }
