import asyncio
import os
from dotenv import load_dotenv
from agentic_framework import Agent, ToolRegistry
from agentic_framework.llm import OpenAIClient
from agentic_framework.tools.search import SearchTool
from agentic_framework.tools.finance import FundamentalAnalysisTool
from agentic_framework.memory.simple import SimpleMemory

load_dotenv()

print("🚀 Advanced Financial Analysis Agent")
print("="*50)

# Setup
llm_client = OpenAIClient(model="gpt-4o-mini")
registry = ToolRegistry()
registry.register(SearchTool())
registry.register(FundamentalAnalysisTool())

# Advanced Financial Analyst Agent
analyst = Agent(
    id="adv_fin_analyst_001",
    name="Advanced Financial Analyst",
    instructions="""
    You are a Senior Financial Analyst. Your goal is to produce a deep-dive investment report for a given company.
    
    IMPORTANT: To use a tool, you MUST use the following format:
    tool_name("argument") or tool_name(arg1="value", arg2="value")
    
    Example:
    fundamental_analysis(ticker="AAPL", detailed=True)
    web_search("latest news about AAPL")
    
    Follow this STRICT workflow:
    1.  **Get Ticker**: Identify the correct ticker symbol for the company.
    2.  **Get Financials**: Use `fundamental_analysis(ticker="...", detailed=True)` to get the Balance Sheet, Income Statement, and Cash Flow.
    3.  **Analyze Data**: 
        - Calculate key growth rates (Revenue, Net Income).
        - Analyze margins (Gross, Operating, Net).
        - Assess financial health (Debt-to-Equity, Current Ratio).
    4.  **Web Search**: Use `web_search` to find recent news, analyst sentiment, and macro trends affecting the sector.
    5.  **Generate Report**: Synthesize ALL data into a professional Markdown report.
        - **Executive Summary**: Buy/Sell/Hold recommendation with rationale.
        - **Company Overview**: Business model and sector.
        - **Financial Analysis**: 
            - Income Statement Highlights (Revenue growth, margins).
            - Balance Sheet Strength (Cash position, debt).
            - Cash Flow Analysis (Operating cash flow trends).
        - **Market Sentiment**: Recent news and analyst views.
        - **Risks**: Potential downsides.
        - **Conclusion**: Final verdict.
    
    Do not skip any steps. Ensure the report is data-driven.
    """,
    tools=registry.get_all(),
    model_client=llm_client,
    memory=SimpleMemory()
)

async def main():
    company = "Tesla"
    print(f"\nStarting Deep Dive Analysis for: {company}...\n")
    
    result = await analyst.execute(f"Perform a deep fundamental analysis on {company}. Generate a comprehensive investment report.")
    
    print("\n" + "="*20 + " Investment Report " + "="*20 + "\n")
    print(result["output"])

if __name__ == "__main__":
    asyncio.run(main())
