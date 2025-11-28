"""Advanced safety guardrails"""
from typing import Any, Dict, List
import re

try:
    from ..core.agent import Agent
    from ..core.tool import Tool
except ImportError:
    pass


class Guardrails:
    """Input/output validation and safety controls"""
    
    DANGEROUS_PATTERNS = [
        r"delete.*data",
        r"drop.*table",
        r"rm\s+-rf",
        r"exec\s*\/bin",
        r"sudo",
        r"password",
        r"secret"
    ]
    
    def __init__(self):
        self.enabled = True
    
    def validate_input(self, task: str) -> bool:
        """Validate input task"""
        if not self.enabled:
            return True
        
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, task.lower()):
                return False
        return True
    
    def validate_tool_call(self, tool: Tool, params: Dict[str, Any]) -> bool:
        """Validate tool parameters"""
        # Tool-specific validation
        if tool.name == "code_executor":
            code = params.get("code", "")
            if any(keyword in code.lower() for keyword in ["import os", "subprocess", "exec"]):
                return False
        return True
    
    def validate_output(self, output: str) -> bool:
        """Validate agent output"""
        return len(output) < 10000  # Prevent token bombs


def add_guardrails(agent: Agent) -> Agent:
    """Add guardrails to agent"""
    agent.guardrails = Guardrails()
    return agent
