import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import DocumentAnalyzer from './pages/DocumentAnalyzer';
import QuestionGenerator from './pages/QuestionGenerator';
import AnswerEvaluator from './pages/AnswerEvaluator';
import LessonPlanner from './pages/LessonPlanner';
import ChatBot from './pages/ChatBot';
import StudentAnalytics from './pages/StudentAnalytics';
import './App.css';

function App() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  return (
    <BrowserRouter>
      <div className="app">
        <Navbar onToggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)} />
        <div className="app-container">
          <Sidebar isOpen={isSidebarOpen} />
          <main className="main-content">
            <Routes>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/document-analyzer" element={<DocumentAnalyzer />} />
              <Route path="/question-generator" element={<QuestionGenerator />} />
              <Route path="/answer-evaluator" element={<AnswerEvaluator />} />
              <Route path="/lesson-planner" element={<LessonPlanner />} />
              <Route path="/chatbot" element={<ChatBot />} />
              <Route path="/student-analytics" element={<StudentAnalytics />} />
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
