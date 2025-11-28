import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import AgentList from './components/AgentList';
import CreateAgentPage from './components/CreateAgentPage';
import AgentExecutionPage from './components/AgentExecutionPage';
import WorkflowBuilder from './components/WorkflowBuilder';
import './index.css';

const API_URL = 'http://127.0.0.1:8000';

function App() {
    const [agents, setAgents] = useState([]);

    useEffect(() => {
        fetchAgents();
    }, []);

    const fetchAgents = async () => {
        try {
            const res = await fetch(`${API_URL}/agents`);
            const data = await res.json();
            setAgents(data);
        } catch (err) {
            console.error("Failed to fetch agents", err);
        }
    };

    return (
        <Router>
            <div className="app-container">
                <Sidebar />
                <div className="main-content-area">
                    <Routes>
                        <Route path="/" element={<AgentList agents={agents} />} />
                        <Route path="/create" element={<CreateAgentPage />} />
                        <Route path="/workflow-builder" element={<WorkflowBuilder />} />
                        <Route path="/agent/:id" element={<AgentExecutionPage />} />
                    </Routes>
                </div>
            </div>
        </Router>
    );
}

export default App;
