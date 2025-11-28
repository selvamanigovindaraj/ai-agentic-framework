import React, { useEffect, useRef } from 'react';
import { Send, Bot, User } from 'lucide-react';

function ChatInterface({ agent, messages, input, setInput, onSend, loading }) {
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, loading]);

    return (
        <div className="chat-interface">
            <div className="chat-header">
                <div className="chat-avatar">
                    {agent.name.substring(0, 2).toUpperCase()}
                </div>
                <div className="chat-title">
                    <h3>{agent.name}</h3>
                    <span>Online • {agent.model}</span>
                </div>
            </div>

            <div className="chat-messages">
                {messages.length === 0 && (
                    <div className="empty-chat">
                        <Bot size={48} className="empty-icon" />
                        <p>Start a conversation with {agent.name}</p>
                    </div>
                )}

                {messages.map((msg, i) => (
                    <div key={i} className={`message-row ${msg.role}`}>
                        <div className="message-avatar">
                            {msg.role === 'agent' ? (
                                <div className="avatar-circle agent">{agent.name.substring(0, 2).toUpperCase()}</div>
                            ) : (
                                <div className="avatar-circle user"><User size={14} /></div>
                            )}
                        </div>
                        <div className="message-bubble">
                            {msg.content}
                        </div>
                    </div>
                ))}

                {loading && (
                    <div className="message-row agent">
                        <div className="message-avatar">
                            <div className="avatar-circle agent">{agent.name.substring(0, 2).toUpperCase()}</div>
                        </div>
                        <div className="message-bubble loading">
                            <span className="typing-dot">.</span>
                            <span className="typing-dot">.</span>
                            <span className="typing-dot">.</span>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            <form className="chat-input-area" onSubmit={onSend}>
                <input
                    className="chat-input"
                    type="text"
                    value={input}
                    onChange={e => setInput(e.target.value)}
                    placeholder={`Message ${agent.name}...`}
                    disabled={loading}
                />
                <button type="submit" className="send-btn" disabled={!input.trim() || loading}>
                    <Send size={18} />
                </button>
            </form>
        </div>
    );
}

export default ChatInterface;
