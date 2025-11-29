import asyncio
import os
from dotenv import load_dotenv
from agentic_framework import Agent, ToolRegistry
from agentic_framework.llm import OpenAIClient
from agentic_framework.tools.finance import FundamentalAnalysisTool
from agentic_framework.tools.search import SearchTool
from agentic_framework.tools.python_repl import PythonREPLTool
from agentic_framework.memory.multilayer import MultiLayerMemory

load_dotenv()

async def main():
    print("🤖 Financial Analyst Multi-Agent Team")
    print("="*50)
    
    # Setup
    llm_client = OpenAIClient(model="gpt-4o-mini")
    memory = MultiLayerMemory()
    
    # Seed Procedural Memory with user preferences
    memory.procedural.set_preference("valuation_style", "Conservative. Cap terminal growth rate at 3%.")
    
    # Create Tool Registry
    finance_registry = ToolRegistry()
    finance_registry.register(FundamentalAnalysisTool())
    
    search_registry = ToolRegistry()
    search_registry.register(SearchTool())
    
    python_registry = ToolRegistry()
    python_registry.register(PythonREPLTool())
    
    # Agent 1: Financial Data Agent
    financial_agent = Agent(
        id="financial_001",
        name="Financial Data Agent",
        instructions="You are a Quantitative Analyst. Fetch financial data (Revenue, Net Income, Cash Flow) for the last 5 years using the fundamental_analysis tool.",
        tools=finance_registry.get_all(),
        model_client=llm_client,
        memory=memory
    )
    
    # Agent 2: Sector Agent
    sector_agent = Agent(
        id="sector_001",
        name="Sector Agent",
        instructions="You are an Industry Analyst. Identify the sector and analyze global market trends using the search tool.",
        tools=search_registry.get_all(),
        model_client=llm_client,
        memory=memory
    )
    
    # Agent 3: Valuation Agent
    valuation_agent = Agent(
        id="valuation_001",
        name="Valuation Agent",
        instructions=f"You are a Valuation Expert. Use Python to calculate DCF valuation. {memory.get_procedural_context()}",
        tools=python_registry.get_all(),
        model_client=llm_client,
        memory=memory
    )
    
    # Agent 4: Critic Agent
    critic_agent = Agent(
        id="critic_001",
        name="The Critic",
        instructions=f"You are a Quality Assurance Critic. Review the analysis and valuation. {memory.get_procedural_context()}",
        tools=[],
        model_client=llm_client,
        memory=memory
    )
    
    # Execute Multi-Agent Workflow
    ticker = "NVDA"
    print(f"\n📊 Analyzing {ticker}...\n")
    
    # Step 1: Financial Data
    print("1️⃣ Financial Data Agent working...")
    financial_result = await financial_agent.execute(f"Fetch financial data for {ticker}")
    print(f"✅ Financial Data: {financial_result['output'][:100]}...\n")
    
    # Step 2: Sector Analysis
    print("2️⃣ Sector Agent working...")
    sector_result = await sector_agent.execute(f"Analyze the sector and market trends for {ticker}")
    print(f"✅ Sector Analysis: {sector_result['output'][:100]}...\n")
    
    # Step 3: Valuation
    print("3️⃣ Valuation Agent working...")
    valuation_context = f"Based on this data:\n{financial_result['output']}\n\nCalculate DCF valuation for {ticker}"
    valuation_result = await valuation_agent.execute(valuation_context)
    print(f"✅ Valuation: {valuation_result['output'][:100]}...\n")
    
    # Step 4: Critic Review
    print("4️⃣ Critic reviewing...")
    critic_context = f"""
    Review this analysis:
    Financial: {financial_result['output'][:200]}
    Sector: {sector_result['output'][:200]}
    Valuation: {valuation_result['output'][:200]}
    """
    critic_result = await critic_agent.execute(critic_context)
    print(f"✅ Critic Review: {critic_result['output'][:200]}...\n")
    
    print("="*50)
    print("✅ Analysis Complete!")

if __name__ == "__main__":
    asyncio.run(main())
