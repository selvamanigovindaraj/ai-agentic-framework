import React from 'react';

export default function WorkflowSidebar() {
    const onDragStart = (event, nodeType) => {
        event.dataTransfer.setData('application/reactflow', nodeType);
        event.dataTransfer.effectAllowed = 'move';
    };

    return (
        <aside className="workflow-sidebar">
            <div className="description">Drag nodes to the canvas</div>

            <div className="dndnode llm" onDragStart={(event) => onDragStart(event, 'llm')} draggable>
                LLM Node
            </div>

            <div className="dndnode tool" onDragStart={(event) => onDragStart(event, 'tool')} draggable>
                Tool Node
            </div>

            <div className="dndnode hitl" onDragStart={(event) => onDragStart(event, 'hitl')} draggable>
                HITL Node
            </div>
        </aside>
    );
}
