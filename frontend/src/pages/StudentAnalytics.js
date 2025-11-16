import React, { useState, useEffect } from 'react';
import { Plus, Trash2, TrendingUp, BarChart3, Users } from 'lucide-react';
import { Line, Bar, Radar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  RadarController,
  Tooltip,
  Legend,
} from 'chart.js';
import './StudentAnalytics.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  RadarController,
  Tooltip,
  Legend
);

function StudentAnalytics() {
  const [students, setStudents] = useState([]);
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [classOverview, setClassOverview] = useState(null);
  const [newStudent, setNewStudent] = useState({ name: '', email: '', grade_level: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showAddStudent, setShowAddStudent] = useState(false);

  const token = localStorage.getItem('token');

  useEffect(() => {
    if (token) {
      loadStudents();
      loadClassOverview();
    }
  }, [token]);

  const loadStudents = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/students/list', {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (response.ok) {
        const data = await response.json();
        setStudents(data);
      }
    } catch (err) {
      console.error('Error loading students:', err);
    }
  };

  const loadClassOverview = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/analytics/class-overview', {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (response.ok) {
        const data = await response.json();
        setClassOverview(data);
      }
    } catch (err) {
      console.error('Error loading class overview:', err);
    }
  };

  const loadStudentAnalytics = async (studentId) => {
    try {
      setLoading(true);
      const response = await fetch(`http://localhost:8000/api/analytics/student/${studentId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (response.ok) {
        const data = await response.json();
        setAnalytics(data);
        setSelectedStudent(studentId);
      }
    } catch (err) {
      setError('Error loading student analytics');
    } finally {
      setLoading(false);
    }
  };

  const handleAddStudent = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/api/students/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(newStudent),
      });

      if (response.ok) {
        setNewStudent({ name: '', email: '', grade_level: '' });
        setShowAddStudent(false);
        loadStudents();
      } else {
        setError('Failed to add student');
      }
    } catch (err) {
      setError('Error adding student');
    }
  };

  const handleDeleteStudent = async (studentId) => {
    if (!window.confirm('Are you sure you want to delete this student?')) return;

    try {
      await fetch(`http://localhost:8000/api/students/${studentId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` },
      });
      loadStudents();
      if (selectedStudent === studentId) {
        setSelectedStudent(null);
        setAnalytics(null);
      }
    } catch (err) {
      setError('Error deleting student');
    }
  };

  // Chart data: Performance trend (recent scores)
  const performanceChartData = analytics?.recent_scores?.length > 0
    ? {
        labels: analytics.recent_scores.map((_, i) => `Score ${i + 1}`).reverse(),
        datasets: [
          {
            label: 'Score Trend',
            data: analytics.recent_scores.map(s => s.score).reverse(),
            borderColor: '#667eea',
            backgroundColor: 'rgba(102, 126, 234, 0.1)',
            tension: 0.4,
            fill: true,
            pointRadius: 5,
            pointHoverRadius: 7,
            pointBackgroundColor: '#667eea',
          },
        ],
      }
    : null;

  // Chart data: Scores by subject
  const subjectChartData = analytics?.scores_by_subject && Object.keys(analytics.scores_by_subject).length > 0
    ? {
        labels: Object.keys(analytics.scores_by_subject),
        datasets: [
          {
            label: 'Average Score by Subject',
            data: Object.values(analytics.scores_by_subject),
            backgroundColor: ['#667eea', '#764ba2', '#10a37f', '#f59e0b', '#ef4444'],
            borderRadius: 8,
            borderSkipped: false,
          },
        ],
      }
    : null;

  // Chart data: Class overview
  const classChartData = classOverview?.class_data?.length > 0
    ? {
        labels: classOverview.class_data.map(s => s.student_name),
        datasets: [
          {
            label: 'Average Score',
            data: classOverview.class_data.map(s => s.average_score),
            backgroundColor: 'rgba(102, 126, 234, 0.8)',
            borderColor: '#667eea',
            borderWidth: 2,
          },
        ],
      }
    : null;

  return (
    <div className="student-analytics">
      <div className="analytics-header">
        <h1>📊 Student Analytics & Performance</h1>
        <button
          className="btn-add-student"
          onClick={() => setShowAddStudent(!showAddStudent)}
        >
          <Plus size={20} /> Add Student
        </button>
      </div>

      {error && <div className="error-banner">{error}</div>}

      {showAddStudent && (
        <div className="add-student-card">
          <form onSubmit={handleAddStudent} className="add-student-form">
            <div className="form-row">
              <div className="form-group">
                <label>Student Name *</label>
                <input
                  type="text"
                  value={newStudent.name}
                  onChange={(e) => setNewStudent({ ...newStudent, name: e.target.value })}
                  placeholder="Full name"
                  required
                />
              </div>
              <div className="form-group">
                <label>Email</label>
                <input
                  type="email"
                  value={newStudent.email}
                  onChange={(e) => setNewStudent({ ...newStudent, email: e.target.value })}
                  placeholder="Email address"
                />
              </div>
              <div className="form-group">
                <label>Grade Level</label>
                <input
                  type="text"
                  value={newStudent.grade_level}
                  onChange={(e) => setNewStudent({ ...newStudent, grade_level: e.target.value })}
                  placeholder="e.g., 9th, 10th"
                />
              </div>
            </div>
            <div className="button-group">
              <button type="submit" className="btn-submit">Add Student</button>
              <button
                type="button"
                className="btn-cancel"
                onClick={() => setShowAddStudent(false)}
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="analytics-container">
        {/* Sidebar: Students list */}
        <div className="students-sidebar">
          <h3>📚 Your Students ({students.length})</h3>
          {students.length === 0 ? (
            <p className="no-students">No students yet. Add your first student!</p>
          ) : (
            <div className="students-list">
              {students.map((student) => (
                <div
                  key={student.id}
                  className={`student-item ${selectedStudent === student.id ? 'active' : ''}`}
                  onClick={() => loadStudentAnalytics(student.id)}
                >
                  <div className="student-info">
                    <span className="student-name">{student.name}</span>
                    <span className="student-grade">{student.grade_level || 'N/A'}</span>
                  </div>
                  <button
                    className="btn-delete"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDeleteStudent(student.id);
                    }}
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Main content: Analytics */}
        <div className="analytics-main">
          {!selectedStudent ? (
            <div className="empty-state">
              <Users size={64} />
              <h2>Select a Student</h2>
              <p>Click on a student to view their performance analytics</p>
            </div>
          ) : loading ? (
            <div className="loading">Loading analytics...</div>
          ) : analytics ? (
            <>
              {/* Student header */}
              <div className="student-header">
                <h2>{analytics.student_name}</h2>
                <div className="student-stats">
                  <div className="stat-card">
                    <span className="stat-label">Total Evaluations</span>
                    <span className="stat-value">{analytics.total_evaluations}</span>
                  </div>
                  <div className="stat-card">
                    <span className="stat-label">Average Score</span>
                    <span className="stat-value highlight">{analytics.average_score}</span>
                  </div>
                  <div className="stat-card">
                    <span className="stat-label">Highest Score</span>
                    <span className="stat-value">{analytics.highest_score}</span>
                  </div>
                  <div className="stat-card">
                    <span className="stat-label">Lowest Score</span>
                    <span className="stat-value">{analytics.lowest_score}</span>
                  </div>
                </div>
              </div>

              {/* Charts */}
              <div className="charts-grid">
                {performanceChartData && (
                  <div className="chart-card">
                    <h3>📈 Performance Trend</h3>
                    <Line
                      data={performanceChartData}
                      options={{
                        responsive: true,
                        plugins: { legend: { display: true } },
                        scales: {
                          y: { beginAtZero: true, max: 100, title: { display: true, text: 'Score' } },
                        },
                      }}
                    />
                  </div>
                )}

                {subjectChartData && (
                  <div className="chart-card">
                    <h3>📊 Scores by Subject</h3>
                    <Bar
                      data={subjectChartData}
                      options={{
                        responsive: true,
                        plugins: { legend: { display: false } },
                        scales: { y: { beginAtZero: true, max: 100 } },
                      }}
                    />
                  </div>
                )}
              </div>

              {/* No data fallback */}
              {!performanceChartData && !subjectChartData && (
                <div className="no-data">
                  <p>No evaluation data yet for this student</p>
                </div>
              )}
            </>
          ) : null}
        </div>
      </div>

      {/* Class Overview */}
      {classOverview && classChartData && (
        <div className="class-overview-section">
          <h2>📊 Class Overview</h2>
          <div className="chart-card large">
            <h3>Class Average Performance</h3>
            <Bar
              data={classChartData}
              options={{
                responsive: true,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true, max: 100 } },
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default StudentAnalytics;
