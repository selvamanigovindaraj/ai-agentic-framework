import React, { useState, useRef, useCallback } from 'react';
import { ReactFlow, ReactFlowProvider, addEdge, useNodesState, useEdgesState, Controls, Background } from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import WorkflowSidebar from './WorkflowSidebar';
import { useNavigate } from 'react-router-dom';

const API_URL = 'http://127.0.0.1:8000';

let id = 0;
const getId = () => `dndnode_${id++}`;

const WorkflowBuilder = () => {
    const reactFlowWrapper = useRef(null);
    const [nodes, setNodes, onNodesChange] = useNodesState([]);
    const [edges, setEdges, onEdgesChange] = useEdgesState([]);
    const [reactFlowInstance, setReactFlowInstance] = useState(null);
    const [agentName, setAgentName] = useState("My Workflow Agent");
    const navigate = useNavigate();

    const onConnect = useCallback((params) => setEdges((eds) => addEdge(params, eds)), []);

    const onDragOver = useCallback((event) => {
        event.preventDefault();
        event.dataTransfer.dropEffect = 'move';
    }, []);

    const onDrop = useCallback(
        (event) => {
            event.preventDefault();

            const type = event.dataTransfer.getData('application/reactflow');

            if (typeof type === 'undefined' || !type) {
                return;
            }

            const position = reactFlowInstance.screenToFlowPosition({
                x: event.clientX,
                y: event.clientY,
            });

            const newNode = {
                id: getId(),
                type: 'default', // Using default for now, can be custom
                position,
                data: { label: `${type} node` },
                style: { border: '1px solid #777', padding: 10, borderRadius: 5, background: '#222', color: '#fff' },
                // Store type in data for backend
                nodeType: type
            };

            setNodes((nds) => nds.concat(newNode));
        },
        [reactFlowInstance],
    );

    const handleSave = async () => {
        const workflowDef = {
            nodes: nodes.map(n => ({
                id: n.id,
                type: n.nodeType || 'llm', // Default to llm if missing
                config: { label: n.data.label } // Simplified config
            })),
            edges: edges.map(e => ({
                source: e.source,
                target: e.target
            }))
        };

        const agentData = {
            name: agentName,
            instructions: "Dynamic Workflow Agent",
            model: "dynamic-workflow",
            workflow: workflowDef
        };

        try {
            const res = await fetch(`${API_URL}/agents`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(agentData)
            });
            const newAgent = await res.json();
            navigate(`/agent/${newAgent.id}`);
        } catch (err) {
            console.error("Failed to save workflow", err);
        }
    };

    return (
        <div className="workflow-builder-page" style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <div className="builder-header" style={{ padding: '16px', borderBottom: '1px solid #333', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <input
                    value={agentName}
                    onChange={(e) => setAgentName(e.target.value)}
                    style={{ background: 'transparent', border: 'none', color: 'white', fontSize: '18px', fontWeight: 'bold' }}
                />
                <button className="primary-btn" onClick={handleSave}>Save & Run</button>
            </div>
            <div className="dndflow" style={{ flex: 1, display: 'flex' }}>
                <ReactFlowProvider>
                    <WorkflowSidebar />
                    <div className="reactflow-wrapper" ref={reactFlowWrapper} style={{ flex: 1, height: '100%' }}>
                        <ReactFlow
                            nodes={nodes}
                            edges={edges}
                            onNodesChange={onNodesChange}
                            onEdgesChange={onEdgesChange}
                            onConnect={onConnect}
                            onInit={setReactFlowInstance}
                            onDrop={onDrop}
                            onDragOver={onDragOver}
                            fitView
                        >
                            <Controls />
                            <Background color="#333" gap={16} />
                        </ReactFlow>
                    </div>
                </ReactFlowProvider>
            </div>
        </div>
    );
};

export default WorkflowBuilder;
