import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
from agentic_framework import Agent, ToolRegistry
from agentic_framework.llm import OpenAIClient
from agentic_framework.tools.search import SearchTool
from agentic_framework.tools.finance import FundamentalAnalysisTool
from agentic_framework.memory.simple import SimpleMemory

print("💰 Financial Analysis Agent Demo")
print("="*50)

# Setup
llm_client = OpenAIClient(model="gpt-4o-mini")
registry = ToolRegistry()
registry.register(SearchTool())
registry.register(FundamentalAnalysisTool())

# Financial Analyst Agent
analyst = Agent(
    id="fin_analyst_001",
    name="Financial Analyst",
    instructions="""
    You are an expert financial analyst. Your goal is to provide a comprehensive analysis of a given stock ticker.
    
    IMPORTANT: To use a tool, you MUST use the following format:
    tool_name("argument")
    
    Example:
    fundamental_analysis("AAPL")
    web_search("latest news about AAPL")
    
    Follow these steps:
    1. Use the 'fundamental_analysis' tool to get key financial metrics and recent news for the ticker.
    2. Use the 'web_search' tool to find any additional context or recent market sentiment if needed.
    3. Synthesize all information into a concise report. Include:
        - Current Price and Market Cap
        - Key Ratios (P/E, Dividend Yield)
        - Analyst Recommendations
        - Recent News Highlights
        - A brief summary of the business
    
    Format your response clearly using Markdown.
    """,
    tools=registry.get_all(),
    model_client=llm_client,
    memory=SimpleMemory()
)

async def main():
    ticker = "AAPL"
    print(f"\nAnalyzing {ticker}...\n")
    
    result = await analyst.execute(f"Analyze the stock {ticker}. Provide a comprehensive report.")
    
    print("\n" + "="*20 + " Analysis Report " + "="*20 + "\n")
    print(result["output"])

if __name__ == "__main__":
    asyncio.run(main())
