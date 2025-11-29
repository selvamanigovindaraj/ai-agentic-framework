from typing import Dict, Any
from agentic_framework.core.tool import Tool, ToolSchema
from agentic_framework.safety.sandbox import DockerSandbox

class PythonREPLTool(Tool):
    """
    Executes Python code in a secure Docker sandbox.
    Useful for complex calculations and data analysis.
    """
    
    def __init__(self):
        super().__init__(
            name="python_repl",
            description="Executes Python code. Use this for math, data analysis, or complex logic. Input should be valid Python code.",
            schema=ToolSchema(
                input_schema={
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "The Python code to execute."
                        }
                    },
                    "required": ["code"]
                },
                output_schema={"type": "string"}
            )
        )
        self.sandbox = DockerSandbox()

    async def execute(self, code: str) -> Dict[str, Any]:
        """Execute code in sandbox"""
        result = self.sandbox.run_code(code)
        return result
