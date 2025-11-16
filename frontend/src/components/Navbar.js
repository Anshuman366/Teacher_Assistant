import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Menu, Settings, LogOut } from 'lucide-react';
import './Navbar.css';

function Navbar({ onToggleSidebar }) {
  const navigate = useNavigate();
  const username = localStorage.getItem('username');

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('username');
    navigate('/auth');
  };

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <button className="menu-button" onClick={onToggleSidebar}>
          <Menu size={24} />
        </button>
        <div className="navbar-brand">
          <div className="brand-icon">📚</div>
          <div className="brand-text">
            <h1>Teacher Assistant</h1>
            <p>AI-Powered Teaching Tool</p>
          </div>
        </div>
      </div>
      <div className="navbar-right">
        {username && <span className="username">👤 {username}</span>}
        <button className="settings-button">
          <Settings size={20} />
        </button>
        <button className="logout-button" onClick={handleLogout} title="Logout">
          <LogOut size={20} />
        </button>
      </div>
    </nav>
  );
}

export default Navbar;
