import React, { useState } from 'react';
import { Brain, Loader, Plus, Trash2 } from 'lucide-react';
import { generateQuestions, generateAnswerKey, generatePracticeQuestions } from '../api';
import MarkdownDisplay from '../components/MarkdownDisplay';
import './QuestionGenerator.css';

function QuestionGenerator() {
  const [content, setContent] = useState('');
  const [numQuestions, setNumQuestions] = useState(5);
  const [difficulty, setDifficulty] = useState('medium');
  const [questionType, setQuestionType] = useState('multiple_choice');
  const [loading, setLoading] = useState(false);
  const [questions, setQuestions] = useState('');
  const [answerKey, setAnswerKey] = useState('');
  const [practiceQuestions, setPracticeQuestions] = useState(null);
  const [activeTab, setActiveTab] = useState('generate');

  const handleGenerateQuestions = async () => {
    if (!content.trim()) {
      alert('Please enter content');
      return;
    }

    setLoading(true);
    try {
      const result = await generateQuestions({
        content,
        num_questions: numQuestions,
        difficulty,
        question_type: questionType
      });
      setQuestions(result.data.questions);
    } catch (error) {
      console.error('Error:', error);
      alert('Error generating questions');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateAnswerKey = async () => {
    if (!content.trim()) {
      alert('Please enter content');
      return;
    }

    setLoading(true);
    try {
      const result = await generateAnswerKey({
        content,
        num_questions: numQuestions
      });
      setAnswerKey(result.data.answer_key);
    } catch (error) {
      console.error('Error:', error);
      alert('Error generating answer key');
    } finally {
      setLoading(false);
    }
  };

  const handleGeneratePracticeQuestions = async () => {
    if (!content.trim()) {
      alert('Please enter content');
      return;
    }

    setLoading(true);
    try {
      const result = await generatePracticeQuestions({
        content,
        num_questions: numQuestions
      });
      setPracticeQuestions(result.data.practice_questions);
    } catch (error) {
      console.error('Error:', error);
      alert('Error generating practice questions');
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    alert('Copied to clipboard!');
  };

  return (
    <div className="question-generator">
      <h1 className="page-title">🧠 Question Generator</h1>
      <p className="page-description">
        Generate high-quality questions, answer keys, and practice materials from your content
      </p>

      <div className="generator-container">
        {/* Input Section */}
        <div className="card input-section">
          <h2>Content & Settings</h2>
          
          <div className="form-group">
            <label>Enter Content or Topic</label>
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="Paste the chapter content, lesson material, or topic you want to generate questions about..."
              rows="6"
              className="content-textarea"
            />
          </div>

          <div className="settings-grid">
            <div className="form-group">
              <label>Number of Questions</label>
              <input
                type="number"
                value={numQuestions}
                onChange={(e) => setNumQuestions(parseInt(e.target.value))}
                min="1"
                max="20"
              />
            </div>

            <div className="form-group">
              <label>Difficulty Level</label>
              <select
                value={difficulty}
                onChange={(e) => setDifficulty(e.target.value)}
              >
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
              </select>
            </div>

            <div className="form-group">
              <label>Question Type</label>
              <select
                value={questionType}
                onChange={(e) => setQuestionType(e.target.value)}
              >
                <option value="multiple_choice">Multiple Choice</option>
                <option value="short_answer">Short Answer</option>
                <option value="essay">Essay</option>
              </select>
            </div>
          </div>

          <div className="button-group">
            <button
              className="btn btn-primary"
              onClick={handleGenerateQuestions}
              disabled={loading}
            >
              {loading ? <Loader className="spinner" /> : <Plus size={18} />}
              Generate Questions
            </button>
            <button
              className="btn btn-secondary"
              onClick={handleGenerateAnswerKey}
              disabled={loading}
            >
              {loading ? <Loader className="spinner" /> : <Plus size={18} />}
              Generate Answer Key
            </button>
            <button
              className="btn btn-secondary"
              onClick={handleGeneratePracticeQuestions}
              disabled={loading}
            >
              {loading ? <Loader className="spinner" /> : <Plus size={18} />}
              Practice Set
            </button>
          </div>
        </div>

        {/* Results Section */}
        {(questions || answerKey || practiceQuestions) && (
          <div className="results-section">
            <div className="tabs">
              {questions && (
                <button
                  className={`tab ${activeTab === 'questions' ? 'active' : ''}`}
                  onClick={() => setActiveTab('questions')}
                >
                  Questions
                </button>
              )}
              {answerKey && (
                <button
                  className={`tab ${activeTab === 'answerkey' ? 'active' : ''}`}
                  onClick={() => setActiveTab('answerkey')}
                >
                  Answer Key
                </button>
              )}
              {practiceQuestions && (
                <button
                  className={`tab ${activeTab === 'practice' ? 'active' : ''}`}
                  onClick={() => setActiveTab('practice')}
                >
                  Practice Questions
                </button>
              )}
            </div>

            <div className="card results-card">
              {activeTab === 'questions' && questions && (
                <div>
                  <h2>Generated Questions</h2>
                  <div className="content-box">
                    <MarkdownDisplay content={questions} />
                  </div>
                  <button
                    className="btn btn-secondary"
                    onClick={() => copyToClipboard(questions)}
                  >
                    Copy to Clipboard
                  </button>
                </div>
              )}

              {activeTab === 'answerkey' && answerKey && (
                <div>
                  <h2>Answer Key</h2>
                  <div className="content-box">
                    <MarkdownDisplay content={answerKey} />
                  </div>
                  <button
                    className="btn btn-secondary"
                    onClick={() => copyToClipboard(answerKey)}
                  >
                    Copy to Clipboard
                  </button>
                </div>
              )}

              {activeTab === 'practice' && practiceQuestions && (
                <div>
                  <h2>Practice Questions by Difficulty</h2>
                  {Object.entries(practiceQuestions).map(([level, qs]) => (
                    <div key={level} className="difficulty-section">
                      <h3>{level.charAt(0).toUpperCase() + level.slice(1)} Level</h3>
                      <div className="content-box">
                        <MarkdownDisplay content={qs} />
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Empty State */}
        {!questions && !answerKey && !practiceQuestions && (
          <div className="empty-state">
            <Brain size={48} />
            <h3>Ready to Generate Questions?</h3>
            <p>Enter your content above and choose your preferred settings</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default QuestionGenerator;
