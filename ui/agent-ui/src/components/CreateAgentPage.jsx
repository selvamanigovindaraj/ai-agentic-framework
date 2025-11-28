import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import AgentBuilder from './AgentBuilder';

const API_URL = 'http://127.0.0.1:8000';

function CreateAgentPage() {
    const navigate = useNavigate();
    const [components, setComponents] = useState({ tools: [], models: [], memory: [], safety: [] });
    const [formData, setFormData] = useState({
        name: '',
        instructions: '',
        model: 'gpt-4o-mini',
        tools: [],
        memory: false,
        safety: true
    });

    useEffect(() => {
        fetchComponents();
    }, []);

    const fetchComponents = async () => {
        try {
            const res = await fetch(`${API_URL}/components`);
            const data = await res.json();
            setComponents(data);
        } catch (err) {
            console.error("Failed to fetch components", err);
        }
    };

    const handleCreateAgent = async (e) => {
        e.preventDefault();
        try {
            const res = await fetch(`${API_URL}/agents`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
            const newAgent = await res.json();
            navigate(`/agent/${newAgent.id}`); // Redirect to execution page
        } catch (err) {
            console.error("Failed to create agent", err);
        }
    };

    return (
        <div className="create-page">
            <AgentBuilder
                formData={formData}
                setFormData={setFormData}
                components={components}
                onSubmit={handleCreateAgent}
                isEditing={false}
            />
        </div>
    );
}

export default CreateAgentPage;
