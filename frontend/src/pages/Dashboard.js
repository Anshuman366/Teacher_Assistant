import React from 'react';
import { useNavigate } from 'react-router-dom';
import { BookOpen, Brain, CheckCircle, Calendar, MessageSquare, Zap } from 'lucide-react';
import './Dashboard.css';
import StudentAnalytics from '../components/StudentAnalytics';

function Dashboard() {
  const navigate = useNavigate();

  const features = [
    {
      icon: BookOpen,
      title: 'Document Analyzer',
      description: 'Upload and analyze documents, get explanations and ask questions',
      path: '/document-analyzer',
      color: '#667eea'
    },
    {
      icon: Brain,
      title: 'Question Generator',
      description: 'Generate practice questions from your teaching materials',
      path: '/question-generator',
      color: '#f093fb'
    },
    {
      icon: CheckCircle,
      title: 'Answer Evaluator',
      description: 'Evaluate student answers with detailed feedback',
      path: '/answer-evaluator',
      color: '#4facfe'
    },
    {
      icon: Calendar,
      title: 'Lesson Planner',
      description: 'Create structured lesson plans with timelines',
      path: '/lesson-planner',
      color: '#43e97b'
    },
    {
      icon: MessageSquare,
      title: 'Chat Bot',
      description: 'Chat with AI about teaching challenges',
      path: '/chatbot',
      color: '#fa709a'
    },
    {
      icon: Zap,
      title: 'Quick Tools',
      description: 'Access frequently used teaching tools',
      path: '/chatbot',
      color: '#30cfd0'
    }
  ];

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1 className="page-title">Welcome to Teacher Assistant Bot 👋</h1>
        <p className="page-description">
          Your AI-powered companion for document analysis, question generation, answer evaluation, 
          lesson planning, and more. Let's make teaching easier and more effective!
        </p>
      </div>

      <div className="features-grid">
        {features.map((feature, index) => {
          const Icon = feature.icon;
          return (
            <div
              key={index}
              className="feature-card"
              onClick={() => navigate(feature.path)}
              style={{ '--card-color': feature.color }}
            >
              <div className="feature-icon-wrapper">
                <Icon size={32} color={feature.color} />
              </div>
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
              <div className="card-arrow">→</div>
            </div>
          );
        })}
      </div>

      <div className="dashboard-info">
        <div className="info-card">
          <h3>🚀 Getting Started</h3>
          <ul>
            <li>Upload documents or images to analyze</li>
            <li>Generate questions and answer keys automatically</li>
            <li>Get AI-powered feedback on student answers</li>
            <li>Create comprehensive lesson plans in minutes</li>
            <li>Chat with AI for teaching advice</li>
          </ul>
        </div>
        <div className="info-card">
          <h3>💡 Tips</h3>
          <ul>
            <li>Use PDF, TXT, or image formats for documents</li>
            <li>Provide clear context for better AI responses</li>
            <li>Customize rubrics for consistent grading</li>
            <li>Save your favorite lesson plans for reuse</li>
            <li>Use chat for quick teaching advice anytime</li>
          </ul>
        </div>

        <div className="info-card analytics-card">
          <h3>📊 Student Analytics</h3>
          <StudentAnalytics data={{ labels: ['Week 1','Week 2','Week 3','Week 4'], scores: [72,78,85,88] }} />
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
