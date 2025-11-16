import React, { useState } from 'react';
import { Calendar, Loader, Plus } from 'lucide-react';
import {
  createLessonPlan,
  createWeekPlan,
  createDailySchedule,
  createAssessmentPlan,
  getResourceRecommendations
} from '../api';
import MarkdownDisplay from '../components/MarkdownDisplay';
import './LessonPlanner.css';

function LessonPlanner() {
  const [planType, setPlanType] = useState('full');
  const [chapterName, setChapterName] = useState('');
  const [topics, setTopics] = useState('');
  const [lecturesPerWeek, setLecturesPerWeek] = useState(3);
  const [totalWeeks, setTotalWeeks] = useState(4);
  const [classLevel, setClassLevel] = useState('high school');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState('');
  const [activeTab, setActiveTab] = useState('full');

  // Additional fields for specific plans
  const [weekNumber, setWeekNumber] = useState(1);
  const [planDate, setPlanDate] = useState('');

  const handleCreateFullLessonPlan = async () => {
    if (!chapterName || !topics.trim()) {
      alert('Please fill in chapter name and topics');
      return;
    }

    const topicsArray = topics.split(',').map(t => t.trim()).filter(t => t);
    
    setLoading(true);
    try {
      const response = await createLessonPlan({
        chapter_name: chapterName,
        topics: topicsArray,
        lectures_per_week: lecturesPerWeek,
        total_weeks: totalWeeks,
        class_level: classLevel
      });
      setResult(response.data.lesson_plan);
      setActiveTab('full');
    } catch (error) {
      console.error('Error:', error);
      alert('Error creating lesson plan');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateWeekPlan = async () => {
    if (!chapterName || !topics.trim()) {
      alert('Please fill in all fields');
      return;
    }

    const topicsArray = topics.split(',').map(t => t.trim()).filter(t => t);
    
    setLoading(true);
    try {
      const response = await createWeekPlan({
        chapter_name: chapterName,
        week_number: weekNumber,
        topics: topicsArray,
        lectures_in_week: lecturesPerWeek
      });
      setResult(response.data.week_plan);
      setActiveTab('week');
    } catch (error) {
      console.error('Error:', error);
      alert('Error creating week plan');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateDailySchedule = async () => {
    if (!chapterName || !topics.trim() || !planDate) {
      alert('Please fill in all fields');
      return;
    }

    const topicsArray = topics.split(',').map(t => t.trim()).filter(t => t);
    
    setLoading(true);
    try {
      const response = await createDailySchedule({
        chapter_name: chapterName,
        date: planDate,
        topics_to_cover: topicsArray,
        duration_minutes: 50
      });
      setResult(response.data.schedule);
      setActiveTab('daily');
    } catch (error) {
      console.error('Error:', error);
      alert('Error creating daily schedule');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateAssessmentPlan = async () => {
    if (!chapterName || !topics.trim()) {
      alert('Please fill in all fields');
      return;
    }

    const topicsArray = topics.split(',').map(t => t.trim()).filter(t => t);
    
    setLoading(true);
    try {
      const response = await createAssessmentPlan({
        chapter_name: chapterName,
        topics: topicsArray,
        total_weeks: totalWeeks,
        assessment_types: ['formative', 'summative']
      });
      setResult(response.data.assessment_plan);
      setActiveTab('assessment');
    } catch (error) {
      console.error('Error:', error);
      alert('Error creating assessment plan');
    } finally {
      setLoading(false);
    }
  };

  const handleGetResources = async () => {
    if (!chapterName || !topics.trim()) {
      alert('Please fill in all fields');
      return;
    }

    const topicsArray = topics.split(',').map(t => t.trim()).filter(t => t);
    
    setLoading(true);
    try {
      const response = await getResourceRecommendations({
        chapter_name: chapterName,
        topics: topicsArray,
        class_level: classLevel
      });
      setResult(response.data.resources);
      setActiveTab('resources');
    } catch (error) {
      console.error('Error:', error);
      alert('Error getting resources');
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    alert('Copied to clipboard!');
  };

  return (
    <div className="lesson-planner">
      <h1 className="page-title">📅 Lesson Planner</h1>
      <p className="page-description">
        Create comprehensive lesson plans, weekly schedules, and assessments
      </p>

      <div className="planner-container">
        {/* Input Form */}
        <div className="card input-form">
          <h2>Lesson Details</h2>

          <div className="form-group">
            <label>Chapter Name</label>
            <input
              type="text"
              value={chapterName}
              onChange={(e) => setChapterName(e.target.value)}
              placeholder="e.g., Introduction to Photosynthesis"
            />
          </div>

          <div className="form-group">
            <label>Topics (comma-separated)</label>
            <textarea
              value={topics}
              onChange={(e) => setTopics(e.target.value)}
              placeholder="e.g., Light reactions, Dark reactions, Chlorophyll"
              rows="3"
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Class Level</label>
              <select value={classLevel} onChange={(e) => setClassLevel(e.target.value)}>
                <option value="high school">High School</option>
                <option value="college">College</option>
                <option value="elementary">Elementary</option>
                <option value="middle school">Middle School</option>
              </select>
            </div>

            <div className="form-group">
              <label>Lectures per Week</label>
              <input
                type="number"
                value={lecturesPerWeek}
                onChange={(e) => setLecturesPerWeek(parseInt(e.target.value))}
                min="1"
                max="10"
              />
            </div>

            <div className="form-group">
              <label>Total Weeks</label>
              <input
                type="number"
                value={totalWeeks}
                onChange={(e) => setTotalWeeks(parseInt(e.target.value))}
                min="1"
                max="52"
              />
            </div>
          </div>

          {/* Additional fields for specific plans */}
          <div className="form-row">
            <div className="form-group">
              <label>Week Number (for week plan)</label>
              <input
                type="number"
                value={weekNumber}
                onChange={(e) => setWeekNumber(parseInt(e.target.value))}
                min="1"
                max="52"
              />
            </div>

            <div className="form-group">
              <label>Date (for daily schedule)</label>
              <input
                type="date"
                value={planDate}
                onChange={(e) => setPlanDate(e.target.value)}
              />
            </div>
          </div>

          {/* Action Buttons */}
          <div className="button-grid">
            <button
              className="btn btn-primary"
              onClick={handleCreateFullLessonPlan}
              disabled={loading}
            >
              {loading ? <Loader className="spinner" /> : <Plus size={18} />}
              Full Lesson Plan
            </button>
            <button
              className="btn btn-secondary"
              onClick={handleCreateWeekPlan}
              disabled={loading}
            >
              {loading ? <Loader className="spinner" /> : <Plus size={18} />}
              Week Plan
            </button>
            <button
              className="btn btn-secondary"
              onClick={handleCreateDailySchedule}
              disabled={loading}
            >
              {loading ? <Loader className="spinner" /> : <Plus size={18} />}
              Daily Schedule
            </button>
            <button
              className="btn btn-secondary"
              onClick={handleCreateAssessmentPlan}
              disabled={loading}
            >
              {loading ? <Loader className="spinner" /> : <Plus size={18} />}
              Assessment Plan
            </button>
            <button
              className="btn btn-secondary"
              onClick={handleGetResources}
              disabled={loading}
            >
              {loading ? <Loader className="spinner" /> : <Plus size={18} />}
              Resources
            </button>
          </div>
        </div>

        {/* Results */}
        {result && (
          <div className="card results-card">
            <div className="result-content">
              <MarkdownDisplay content={result} />
            </div>
            <button
              className="btn btn-secondary"
              onClick={() => copyToClipboard(result)}
            >
              Copy to Clipboard
            </button>
          </div>
        )}

        {/* Empty State */}
        {!result && (
          <div className="empty-state">
            <Calendar size={48} />
            <h3>Create Your Lesson Plan</h3>
            <p>Fill in the details and choose the type of plan you want to create</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default LessonPlanner;
