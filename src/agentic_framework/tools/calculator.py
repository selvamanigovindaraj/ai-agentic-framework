class Calculator(Tool):
    """Basic calculator tool"""
    
    def __init__(self):
        super().__init__(
            name="calculator",
            description="Perform basic math operations (+, -, *, /, sqrt)",
            category="math"
        )
    
    async def execute(self, operation: str, a: float, b: float = None) -> float:
        """Execute math operation"""
        if operation == "add":
            return a + b
        elif operation == "subtract":
            return a - b
        elif operation == "multiply":
            return a * b
        elif operation == "divide":
            return a / b if b != 0 else float("inf")
        elif operation == "sqrt" and b is None:
            import math
            return math.sqrt(a)
        raise ValueError(f"Unknown operation: {operation}")
