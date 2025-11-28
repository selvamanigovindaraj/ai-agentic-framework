from typing import List, Dict, Any
from ddgs import DDGS
from agentic_framework.core.tool import Tool

class SearchTool(Tool):
    """Tool for performing web searches using DuckDuckGo."""
    
    def __init__(self, max_results: int = 5):
        super().__init__(
            name="web_search",
            description="Search the web for information about a topic or ticker.",
            category="search"
        )
        self.max_results = max_results
    
    async def execute(self, query: str) -> List[Dict[str, Any]]:
        """
        Execute a web search.
        
        Args:
            query: The search query string
            
        Returns:
            List of search results containing title, link, and snippet
        """
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=self.max_results))
                return results
        except Exception as e:
            return [{"error": f"Search failed: {str(e)}"}]
