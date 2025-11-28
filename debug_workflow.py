import asyncio
from agentic_framework.workflows.dynamic_workflow import DynamicWorkflow
from dotenv import load_dotenv

load_dotenv()

async def main():
    workflow_def = {
        "nodes": [
            {"id": "1", "type": "llm", "config": {"label": "Analyze Sector", "prompt": "Analyze the sector for {input}"}},
            {"id": "2", "type": "hitl", "config": {"label": "Confirm", "message": "Confirm"}}
        ],
        "edges": [
            {"source": "1", "target": "2"}
        ]
    }
    
    try:
        workflow = DynamicWorkflow(workflow_def)
        app = workflow.build_graph()
        
        initial_state = {
            "input": "AAPL", 
            "messages": [], 
            "context": {}, 
            "current_node": "start", 
            "status": "started"
        }
        
        print("Starting execution...")
        config = {"configurable": {"thread_id": "test_thread"}}
        result = await app.ainvoke(initial_state, config=config)
        print("Execution result:", result)
        
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
