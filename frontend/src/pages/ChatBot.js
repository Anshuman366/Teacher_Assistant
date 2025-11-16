import React, { useState, useRef, useEffect } from 'react';
import { Send, Upload, Loader, MessageCircle, Plus, Trash2 } from 'lucide-react';
import { sendChatMessage } from '../api';
import MarkdownDisplay from '../components/MarkdownDisplay';
import './ChatBot.css';

function ChatBot() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [uploadedDocs, setUploadedDocs] = useState([]);
  const [showSidebar, setShowSidebar] = useState(true);
  const [selectedDoc, setSelectedDoc] = useState(null);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (messages.length === 0) {
      setMessages([
        {
          id: 1,
          type: 'bot',
          content: 'Hello! I\'m your Teacher Assistant. Upload documents to get started, or ask me anything about teaching, curriculum, classroom management, assessment, or differentiation strategies.'
        }
      ]);
    }
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      if (data.status === 'success') {
        setUploadedDocs(prev => [...prev, {
          id: Date.now(),
          name: data.filename,
          size: data.size,
          type: data.file_type
        }]);

        const botMessage = {
          id: messages.length + 1,
          type: 'bot',
          content: `✓ Document "${data.filename}" uploaded successfully! Now you can ask me questions about this document.`
        };
        setMessages(prev => [...prev, botMessage]);
      }
    } catch (error) {
      console.error('Upload error:', error);
      const errorMessage = {
        id: messages.length + 1,
        type: 'bot',
        content: 'Failed to upload document. Please try again.'
      };
      setMessages(prev => [...prev, errorMessage]);
    }
    
    event.target.value = '';
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage = {
      id: messages.length + 1,
      type: 'user',
      content: inputValue
    };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setLoading(true);

    try {
      const response = await sendChatMessage({
        message: inputValue,
        use_rag: uploadedDocs.length > 0,
        selected_document: selectedDoc
      });

      const botMessage = {
        id: messages.length + 2,
        type: 'bot',
        content: response.data.response || response.data.message || 'I understood your question. Let me help you.'
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = {
        id: messages.length + 2,
        type: 'bot',
        content: 'Sorry, I encountered an error. Please try again.'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleNewChat = () => {
    setMessages([
      {
        id: 1,
        type: 'bot',
        content: 'Hello! I\'m your Teacher Assistant. Upload documents to get started, or ask me anything about teaching.'
      }
    ]);
  };

  const handleDeleteDoc = (docId) => {
    setUploadedDocs(prev => prev.filter(doc => doc.id !== docId));
    if (selectedDoc && selectedDoc.id === docId) {
      setSelectedDoc(null);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="chatbot-gpt">
      {/* Sidebar */}
      <div className={`gpt-sidebar ${showSidebar ? 'open' : 'closed'}`}>
        <div className="sidebar-header">
          <button className="new-chat-btn" onClick={handleNewChat}>
            <Plus size={20} /> New Chat
          </button>
        </div>

        <div className="documents-section">
          <h3>📄 Documents</h3>
          {uploadedDocs.length === 0 ? (
            <p className="no-docs">No documents uploaded yet</p>
          ) : (
            <div className="docs-list">
              {uploadedDocs.map(doc => (
                <div
                  key={doc.id}
                  className={`doc-item ${selectedDoc?.id === doc.id ? 'active' : ''}`}
                  onClick={() => setSelectedDoc(doc)}
                >
                  <span className="doc-name">{doc.name}</span>
                  <button
                    className="delete-btn"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDeleteDoc(doc.id);
                    }}
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="sidebar-footer">
          <button
            className="upload-btn"
            onClick={() => fileInputRef.current?.click()}
          >
            <Upload size={18} /> Upload Document
          </button>
          <input
            ref={fileInputRef}
            type="file"
            onChange={handleFileUpload}
            accept=".pdf,.txt,.doc,.docx,.jpg,.jpeg,.png"
            style={{ display: 'none' }}
          />
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="chatbot-main">
        {/* Messages */}
        <div className="messages-area">
          {messages.length === 0 ? (
            <div className="empty-state">
              <MessageCircle size={48} />
              <h2>Start a New Conversation</h2>
              <p>Upload documents and ask questions, or chat about teaching topics</p>
            </div>
          ) : (
            <>
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`chat-message ${message.type}`}
                >
                  <div className="message-avatar">
                    {message.type === 'user' ? '👤' : '🤖'}
                  </div>
                  <div className="message-body">
                    {message.type === 'bot' ? (
                      <MarkdownDisplay content={message.content} />
                    ) : (
                      <p>{message.content}</p>
                    )}
                  </div>
                </div>
              ))}
              {loading && (
                <div className="chat-message bot">
                  <div className="message-avatar">🤖</div>
                  <div className="message-body">
                    <div className="loading-message">
                      <Loader className="spinner" size={16} />
                      <span>Thinking...</span>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </>
          )}
        </div>

        {/* Input Area */}
        <div className="input-section">
          {selectedDoc && (
            <div className="selected-doc-info">
              📎 Using: <strong>{selectedDoc.name}</strong>
              <button onClick={() => setSelectedDoc(null)}>×</button>
            </div>
          )}
          <div className="input-wrapper">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Message Teacher Assistant..."
              rows="1"
              className="chat-textarea"
            />
            <button
              className="send-btn"
              onClick={handleSendMessage}
              disabled={!inputValue.trim() || loading}
            >
              <Send size={20} />
            </button>
          </div>
          <p className="footer-text">Teacher Assistant uses AI to provide teaching guidance. Always review advice for your specific context.</p>
        </div>
      </div>
    </div>
  );
}

export default ChatBot;
