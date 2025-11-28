import asyncio
import os
from dotenv import load_dotenv
from agentic_framework import Agent, ToolRegistry
from agentic_framework.llm import OpenAIClient
from agentic_framework.core.tool import Tool
from agentic_framework.safety.sandbox import DockerSandbox
from agentic_framework.safety.guardrails import Guardrails
from agentic_framework.safety.audit import AuditLogger

load_dotenv()

print("🔒 Secure Agent System")
print("="*50)

# Setup
llm_client = OpenAIClient(model="gpt-4o-mini")
sandbox = DockerSandbox()
audit = AuditLogger()

# Define a Secure Tool
class CodeRunnerTool(Tool):
    def __init__(self):
        super().__init__("run_code", "Run Python code securely", "dev")
        
    @Guardrails.input_filter(forbidden_patterns=[r"rm\s+-rf", r"os\.system"])
    async def execute(self, code: str) -> str:
        audit.log_event("TOOL_EXECUTION", "secure_agent", {"tool": "run_code", "code": code})
        print(f"🔒 Executing code in Sandbox: {code}")
        result = sandbox.run_code(code)
        return result.get("output", result.get("error"))

# Create Agent
agent = Agent(
    id="secure_agent",
    name="Secure Developer",
    instructions="You are a secure coding assistant. Use run_code to execute Python.",
    tools=[CodeRunnerTool()],
    model_client=llm_client
)

from agentic_framework.orchestration.workflow import WorkflowGraph, Orchestrator
from langgraph.graph import END

# ... (Previous imports and setup remain)

import sys

async def main():
    # Check for auto mode (for automated testing)
    auto_mode = "--auto" in sys.argv
    
    # 1. Safe Execution
    print("\n✅ Testing Safe Execution...")
    result1 = await agent._execute_tool({"tool": agent.tools[0], "params": {"code": "print(2 + 2)"}})
    print(f"Result: {result1}")
    
    # 2. Unsafe Execution
    print("\n🚫 Testing Unsafe Execution (Guardrail)...")
    try:
        await agent._execute_tool({"tool": agent.tools[0], "params": {"code": "import os; os.system('rm -rf /')"}})
    except ValueError as e:
        print(f"Caught Expected Error: {e}")
        audit.log_event("SECURITY_VIOLATION", "secure_agent", {"error": str(e)})
    
    # 3. Extensive HITL
    print("\n🚧 Testing Extensive Human-in-the-Loop (HITL)...")
    
    workflow = WorkflowGraph()
    workflow.add_node("developer", agent, interrupt_before=True)
    workflow.set_entry_point("developer")
    workflow.add_edge("developer", END)
    
    orchestrator = Orchestrator(workflow)
    thread_id = "hitl-demo-extensive"
    
    print(f"Starting workflow (Thread: {thread_id})...")
    
    # Initial run
    result = await orchestrator.execute("Write a python script to print 'Hello HITL'", context={"thread_id": thread_id})
    
    # HITL Loop
    while True:
        # Check if finished
        if result["success"] and not result["output"].get("__interrupt__"):
             # Note: LangGraph returns the state. If it finished, we are done.
             # But wait, interrupt_before stops BEFORE the node.
             # So the state is "pending execution of developer".
             pass

        print("\n⏸️  Workflow Paused. Next node: 'developer'")
        print("Options:")
        print("  [c] Continue (Approve)")
        print("  [f] Feedback (Reject & Retry)")
        print("  [q] Quit")
        
        if auto_mode:
            print("🤖 Auto-Mode: Providing feedback first, then approving.")
            # Simulate feedback loop
            if "Hello HITL" not in str(result): # First pass
                choice = "f"
                feedback = "Make it print 'Hello Secure World' instead."
            else:
                choice = "c"
        else:
            choice = input("Select option: ").lower()
        
        if choice == "q":
            print("Quitting.")
            break
            
        elif choice == "c":
            print("✅ Approving... Resuming workflow.")
            # Resume with None input (just continue)
            result = await orchestrator.execute(None, context={"thread_id": thread_id})
            
            if result["success"]:
                final = result["output"]
                # Check if we are done (no more interrupts)
                # In this simple graph, after developer it goes to END.
                print("\n🎉 Workflow Completed!")
                # Extract last message
                msgs = final.get("messages", [])
                if msgs:
                    print(f"Final Output: {msgs[-1]['content']}")
                break
                
        elif choice == "f":
            if auto_mode:
                print(f"📝 Sending Feedback: {feedback}")
            else:
                feedback = input("Enter feedback: ")
            
            print("🔄 Updating state with feedback and resuming...")
            # Inject feedback as a user message
            update = {
                "messages": [{"role": "user", "content": f"Feedback: {feedback}"}]
            }
            # We call execute with the update. 
            # LangGraph will append this message and THEN try to run the node again?
            # Actually, interrupt_before stops BEFORE the node.
            # If we add a message, we want the agent to see it.
            # But the agent is the NEXT node.
            # So we are essentially modifying the state passed TO the agent.
            result = await orchestrator.execute(update, context={"thread_id": thread_id})
            # Loop continues to see if it pauses again (it shouldn't if we removed interrupt, but interrupt is configured on the node)
            # Wait, interrupt_before=True means it ALWAYS pauses before that node?
            # Yes, if configured in compile.
            # So it will pause AGAIN.
            # This allows us to verify the agent's *planned* action if we had a planner.
            # Here, 'developer' IS the agent.
            # So we provide feedback, it pauses again before executing 'developer' with the new context?
            # Let's see.
            
if __name__ == "__main__":
    asyncio.run(main())
