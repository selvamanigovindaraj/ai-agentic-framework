import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Bot, Plus, ArrowRight } from 'lucide-react';

function AgentList({ agents }) {
    const navigate = useNavigate();

    return (
        <div className="dashboard-page">
            <div className="page-header">
                <div>
                    <h2>Your Agents</h2>
                    <p>Manage and monitor your AI agents</p>
                </div>
                <button className="primary-btn" onClick={() => navigate('/create')}>
                    <Plus size={18} />
                    Create New Agent
                </button>
            </div>

            <div className="agents-grid">
                {agents.length === 0 ? (
                    <div className="empty-state">
                        <Bot size={48} className="empty-icon" />
                        <h3>No Agents Yet</h3>
                        <p>Create your first AI agent to get started.</p>
                        <button className="secondary-btn" onClick={() => navigate('/create')}>
                            Create Agent
                        </button>
                    </div>
                ) : (
                    agents.map(agent => (
                        <div key={agent.id} className="agent-card" onClick={() => navigate(`/agent/${agent.id}`)}>
                            <div className="agent-card-header">
                                <div className="agent-avatar">
                                    {agent.name.substring(0, 2).toUpperCase()}
                                </div>
                                <div className="agent-info">
                                    <h3>{agent.name}</h3>
                                    <span className="agent-model">{agent.model}</span>
                                </div>
                            </div>
                            <div className="agent-card-body">
                                <p>{agent.instructions.substring(0, 100)}...</p>
                            </div>
                            <div className="agent-card-footer">
                                <span className="tool-count">{agent.tools.length} Tools</span>
                                <ArrowRight size={16} className="arrow-icon" />
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
}

export default AgentList;
