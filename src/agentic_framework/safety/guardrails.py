"""Advanced safety guardrails using Decorators"""
from typing import Callable, Any, Dict, List
import functools
import re

class Guardrails:
    """Input/Output validation and safety controls"""
    
    DANGEROUS_PATTERNS = [
        r"delete.*data",
        r"drop.*table",
        r"rm\s+-rf",
        r"exec\s*\/bin",
        r"sudo",
        r"password",
        r"secret",
        r"os\.system"
    ]
    
    @staticmethod
    def input_filter(forbidden_patterns: List[str] = None):
        """Decorator to validate input arguments"""
        patterns = (forbidden_patterns or []) + Guardrails.DANGEROUS_PATTERNS
        
        def decorator(func: Callable):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                # Check args and kwargs strings
                all_inputs = [str(a) for a in args] + [str(v) for v in kwargs.values()]
                for inp in all_inputs:
                    for pattern in patterns:
                        if re.search(pattern, inp, re.IGNORECASE):
                            raise ValueError(f"Security Violation: Input contains forbidden pattern '{pattern}'")
                return await func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def output_filter(max_length: int = 10000):
        """Decorator to validate output"""
        def decorator(func: Callable):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                result = await func(*args, **kwargs)
                if isinstance(result, str) and len(result) > max_length:
                    return result[:max_length] + "... (Truncated for security)"
                return result
            return wrapper
        return decorator
