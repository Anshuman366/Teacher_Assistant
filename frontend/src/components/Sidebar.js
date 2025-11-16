import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Menu, BookOpen, Brain, CheckCircle, Calendar, MessageSquare, Home, BarChart3 } from 'lucide-react';
import './Sidebar.css';

function Sidebar({ isOpen }) {
  const location = useLocation();

  const menuItems = [
    { path: '/dashboard', label: 'Dashboard', icon: Home },
    { path: '/student-analytics', label: 'Student Analytics', icon: BarChart3 },
    { path: '/document-analyzer', label: 'Document Analyzer', icon: BookOpen },
    { path: '/question-generator', label: 'Question Generator', icon: Brain },
    { path: '/answer-evaluator', label: 'Answer Evaluator', icon: CheckCircle },
    { path: '/lesson-planner', label: 'Lesson Planner', icon: Calendar },
    { path: '/chatbot', label: 'Chat Bot', icon: MessageSquare },
  ];

  return (
    <aside className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
      <nav className="sidebar-nav">
        {menuItems.map((item) => {
          const Icon = item.icon;
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
            >
              <Icon size={20} />
              <span className="nav-label">{item.label}</span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}

export default Sidebar;
