import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import ChatInterface from './ChatInterface';

const API_URL = 'http://127.0.0.1:8000';

function AgentExecutionPage() {
    const { id } = useParams();
    const [agent, setAgent] = useState(null);
    const [messages, setMessages] = useState([]);
    const [chatInput, setChatInput] = useState('');
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        // Fetch specific agent (simulated by fetching all and filtering for now, ideally backend has get-by-id)
        fetchAgents();
    }, [id]);

    const fetchAgents = async () => {
        try {
            const res = await fetch(`${API_URL}/agents`);
            const data = await res.json();
            const found = data.find(a => a.id === id);
            if (found) {
                setAgent(found);
                setMessages([{ role: 'agent', content: `Hello! I am ${found.name}. How can I help you?` }]);
            }
        } catch (err) {
            console.error("Failed to fetch agent", err);
        }
    };

    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!chatInput.trim() || !agent) return;

        const userMsg = { role: 'user', content: chatInput };
        setMessages(prev => [...prev, userMsg]);
        setChatInput('');
        setLoading(true);

        try {
            const res = await fetch(`${API_URL}/agents/${agent.id}/execute`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ task: chatInput })
            });
            const data = await res.json();

            const agentMsg = {
                role: 'agent',
                content: data.success ? String(data.output) : `Error: ${data.error}`
            };
            setMessages(prev => [...prev, agentMsg]);
        } catch (err) {
            setMessages(prev => [...prev, { role: 'agent', content: "Network Error" }]);
        } finally {
            setLoading(false);
        }
    };

    if (!agent) return <div className="loading-state">Loading Agent...</div>;

    return (
        <div className="execution-page">
            <ChatInterface
                agent={agent}
                messages={messages}
                input={chatInput}
                setInput={setChatInput}
                onSend={handleSendMessage}
                loading={loading}
            />
        </div>
    );
}

export default AgentExecutionPage;
