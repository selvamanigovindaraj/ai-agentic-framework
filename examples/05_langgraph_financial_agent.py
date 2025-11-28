import asyncio
import os
from dotenv import load_dotenv
from agentic_framework import Agent, ToolRegistry
from agentic_framework.llm import OpenAIClient
from agentic_framework.tools.search import SearchTool
from agentic_framework.tools.finance import FundamentalAnalysisTool
from agentic_framework.orchestration.workflow import WorkflowGraph, Orchestrator
from langgraph.graph import END

load_dotenv()

print("🔗 LangGraph Financial Agent System")
print("="*50)

# Setup
llm_client = OpenAIClient(model="gpt-4o-mini")
registry = ToolRegistry()
registry.register(SearchTool())
registry.register(FundamentalAnalysisTool())

# --- Define Agents ---

# 1. Researcher Agent
researcher = Agent(
    id="researcher",
    name="Market Researcher",
    instructions="""
    You are a Market Researcher. Your goal is to find the latest news and market sentiment for a given company.
    Use the `web_search` tool.
    Output a summary of recent news and sentiment.
    """,
    tools=[registry.get("web_search")],
    model_client=llm_client
)

# 2. Financial Analyst Agent
analyst = Agent(
    id="analyst",
    name="Financial Analyst",
    instructions="""
    You are a Financial Analyst. Your goal is to analyze the financial health of a company.
    Use the `fundamental_analysis` tool with `detailed=True`.
    Output a summary of key financial metrics (Revenue, Margins, Debt).
    """,
    tools=[registry.get("fundamental_analysis")],
    model_client=llm_client
)

# 3. Report Writer Agent
writer = Agent(
    id="writer",
    name="Report Writer",
    instructions="""
    You are a Senior Investment Writer. 
    Your goal is to synthesize the research and financial analysis into a final investment report.
    
    You will receive input from the Researcher and the Analyst.
    Combine them into a cohesive Markdown report with:
    - Executive Summary
    - Market Sentiment (from Researcher)
    - Financial Health (from Analyst)
    - Conclusion (Buy/Sell/Hold)
    """,
    tools=[], # Writer just synthesizes
    model_client=llm_client
)

# --- Build LangGraph Workflow ---

workflow = WorkflowGraph()

# Add Nodes
workflow.add_node("researcher", researcher)
workflow.add_node("analyst", analyst)
workflow.add_node("writer", writer)

# Add Edges (Linear Flow: Researcher -> Analyst -> Writer -> END)
# Note: In a real graph, Researcher and Analyst could run in parallel
workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "analyst")
workflow.add_edge("analyst", "writer")
workflow.add_edge("writer", END)

# Create Orchestrator
orchestrator = Orchestrator(workflow)

async def main():
    company = "Microsoft"
    print(f"\nStarting Multi-Agent Analysis for: {company}...\n")
    
    result = await orchestrator.execute(f"Analyze {company}")
    
    if result["success"]:
        final_state = result["output"]
        # The writer's output should be the last message from the 'writer' node
        # But for now, let's just print the last message in the state
        last_message = final_state["messages"][-1]
        print("\n" + "="*20 + " Final Report " + "="*20 + "\n")
        print(last_message["content"])
    else:
        print(f"Workflow failed: {result['error']}")

if __name__ == "__main__":
    asyncio.run(main())
