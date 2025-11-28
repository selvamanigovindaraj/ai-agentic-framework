"""Tool Registry for dynamic discovery"""
from typing import Dict, List, Optional
from ..core.tool import Tool


class ToolRegistry:
    """Centralized tool registry with semantic discovery"""
    
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self.categories: Dict[str, List[str]] = {}
    
    def register(self, tool: Tool) -> None:
        """Register a tool"""
        self.tools[tool.id] = tool
        
        if tool.category not in self.categories:
            self.categories[tool.category] = []
        self.categories[tool.category].append(tool.id)
        
        print(f"✅ Registered tool: {tool.name} (ID: {tool.id})")
    
    def get(self, tool_id: str) -> Optional[Tool]:
        """Get tool by ID"""
        return self.tools.get(tool_id)
    
    def get_all(self) -> List[Tool]:
        """Get all registered tools"""
        return list(self.tools.values())
    
    def discover(self, query: str, filters: Optional[Dict] = None) -> List[Tool]:
        """Discover tools by query and filters"""
        results = []
        
        for tool in self.tools.values():
            if (query.lower() in tool.name.lower() or 
                query.lower() in tool.description.lower()):
                
                if filters:
                    if "category" in filters and tool.category != filters["category"]:
                        continue
                
                results.append(tool)
        
        return results
    
    def list_categories(self) -> List[str]:
        """List all tool categories"""
        return list(self.categories.keys())
    
    def get_by_category(self, category: str) -> List[Tool]:
        """Get tools by category"""
        tool_ids = self.categories.get(category, [])
        return [self.tools[tid] for tid in tool_ids if tid in self.tools]
