import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutGrid, Plus, Bot } from 'lucide-react';

function Sidebar() {
    return (
        <div className="sidebar">
            <div className="brand">
                <LayoutGrid className="brand-icon" size={24} />
                <span>Agentic AI</span>
            </div>

            <nav className="nav-menu">
                <NavLink to="/" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                    <LayoutGrid size={18} />
                    <span>Dashboard</span>
                </NavLink>

                <NavLink to="/create" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                    <Plus size={18} />
                    <span>Create Agent</span>
                </NavLink>

                <NavLink to="/workflow-builder" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                    <LayoutGrid size={18} />
                    <span>Visual Builder</span>
                </NavLink>
            </nav>

            <div className="sidebar-footer">
                <div className="user-info">
                    <div className="user-avatar">U</div>
                    <div className="user-details">
                        <span className="user-name">User</span>
                        <span className="user-role">Admin</span>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Sidebar;
