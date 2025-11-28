import React from 'react';
import { Save, Cpu, Shield, Brain, Wrench } from 'lucide-react';

function AgentBuilder({ formData, setFormData, components, onSubmit, isEditing }) {
    const toggleTool = (toolId) => {
        setFormData(prev => {
            const tools = prev.tools.includes(toolId)
                ? prev.tools.filter(t => t !== toolId)
                : [...prev.tools, toolId];
            return { ...prev, tools };
        });
    };

    return (
        <div className="builder-form">
            <div className="form-header">
                <h2>{isEditing ? 'Edit Agent' : 'Create New Agent'}</h2>
                <p>Configure your AI agent's personality, capabilities, and safety protocols.</p>
            </div>

            <form onSubmit={onSubmit}>
                <div className="form-group">
                    <label>Agent Name</label>
                    <input
                        className="form-input"
                        type="text"
                        value={formData.name}
                        onChange={e => setFormData({ ...formData, name: e.target.value })}
                        placeholder="e.g., Financial Analyst Bot"
                        required
                    />
                </div>

                <div className="form-group">
                    <label>Instructions (System Prompt)</label>
                    <textarea
                        className="form-textarea"
                        rows="4"
                        value={formData.instructions}
                        onChange={e => setFormData({ ...formData, instructions: e.target.value })}
                        placeholder="Describe how the agent should behave..."
                        required
                    />
                </div>

                <div className="form-group">
                    <label>Model</label>
                    <select
                        className="form-select"
                        value={formData.model}
                        onChange={e => setFormData({ ...formData, model: e.target.value })}
                    >
                        {components.models.map(m => <option key={m} value={m}>{m}</option>)}
                    </select>
                </div>

                <div className="form-group">
                    <label><Wrench size={16} style={{ display: 'inline', marginRight: '6px' }} /> Tools</label>
                    <div className="checkbox-grid">
                        {components.tools.map(tool => (
                            <div
                                key={tool.id}
                                className={`checkbox-card ${formData.tools.includes(tool.id) ? 'checked' : ''}`}
                                onClick={() => toggleTool(tool.id)}
                            >
                                <input
                                    type="checkbox"
                                    checked={formData.tools.includes(tool.id)}
                                    readOnly
                                />
                                <div className="checkbox-info">
                                    <span className="checkbox-label">{tool.name}</span>
                                    <span className="checkbox-desc">{tool.description}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="form-group">
                    <label>Advanced Capabilities</label>
                    <div className="checkbox-grid">
                        <div
                            className={`checkbox-card ${formData.memory ? 'checked' : ''}`}
                            onClick={() => setFormData({ ...formData, memory: !formData.memory })}
                        >
                            <Brain size={20} className={formData.memory ? 'text-accent' : ''} />
                            <div className="checkbox-info">
                                <span className="checkbox-label">Long-term Memory</span>
                                <span className="checkbox-desc">Enable multi-layer memory</span>
                            </div>
                        </div>

                        <div
                            className={`checkbox-card ${formData.safety ? 'checked' : ''}`}
                            onClick={() => setFormData({ ...formData, safety: !formData.safety })}
                        >
                            <Shield size={20} className={formData.safety ? 'text-accent' : ''} />
                            <div className="checkbox-info">
                                <span className="checkbox-label">Safety Layer</span>
                                <span className="checkbox-desc">Guardrails & Sandboxing</span>
                            </div>
                        </div>
                    </div>
                </div>

                {!isEditing && (
                    <button type="submit" className="new-agent-btn" style={{ width: '100%', marginTop: '1rem' }}>
                        <Save size={18} />
                        Create Agent
                    </button>
                )}
            </form>
        </div>
    );
}

export default AgentBuilder;
