import React, { useState } from 'react';
import { CheckCircle, Upload, Loader } from 'lucide-react';
import { evaluateAnswer, evaluateImage, bulkEvaluateAnswers } from '../api';
import MarkdownDisplay from '../components/MarkdownDisplay';
import './AnswerEvaluator.css';

function AnswerEvaluator() {
  const [evaluationType, setEvaluationType] = useState('text');
  const [question, setQuestion] = useState('');
  const [studentAnswer, setStudentAnswer] = useState('');
  const [correctAnswer, setCorrectAnswer] = useState('');
  const [evaluation, setEvaluation] = useState('');
  const [loading, setLoading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [answerExplanation, setAnswerExplanation] = useState('');

  const handleEvaluateAnswer = async () => {
    if (!question || !studentAnswer) {
      alert('Please fill in all fields');
      return;
    }

    setLoading(true);
    try {
      const result = await evaluateAnswer({
        question,
        student_answer: studentAnswer,
        correct_answer: correctAnswer
      });
      setEvaluation(result.data.evaluation);
    } catch (error) {
      console.error('Error:', error);
      alert('Error evaluating answer');
    } finally {
      setLoading(false);
    }
  };

  const handleEvaluateImage = async () => {
    if (!uploadedFile || !question) {
      alert('Please upload an image and enter a question');
      return;
    }

    setLoading(true);
    try {
      const result = await evaluateImage(uploadedFile, question, answerExplanation);
      setEvaluation(result.data.evaluation);
    } catch (error) {
      console.error('Error:', error);
      alert('Error evaluating image');
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setUploadedFile(file);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    alert('Copied to clipboard!');
  };

  return (
    <div className="answer-evaluator">
      <h1 className="page-title">✅ Answer Evaluator</h1>
      <p className="page-description">
        Evaluate student answers with detailed feedback and scoring
      </p>

      <div className="evaluator-container">
        {/* Type Selection */}
        <div className="card type-selector">
          <h2>Evaluation Type</h2>
          <div className="type-buttons">
            <button
              className={`type-btn ${evaluationType === 'text' ? 'active' : ''}`}
              onClick={() => setEvaluationType('text')}
            >
              <span>📝</span>
              Text Answer
            </button>
            <button
              className={`type-btn ${evaluationType === 'image' ? 'active' : ''}`}
              onClick={() => setEvaluationType('image')}
            >
              <span>📸</span>
              Image Answer
            </button>
            <button
              className={`type-btn ${evaluationType === 'bulk' ? 'active' : ''}`}
              onClick={() => setEvaluationType('bulk')}
            >
              <span>📊</span>
              Bulk Evaluate
            </button>
          </div>
        </div>

        {/* Text Answer Evaluation */}
        {evaluationType === 'text' && (
          <div className="card evaluation-form">
            <h2>Evaluate Text Answer</h2>

            <div className="form-group">
              <label>Question</label>
              <textarea
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Enter the question..."
                rows="3"
              />
            </div>

            <div className="form-group">
              <label>Student's Answer</label>
              <textarea
                value={studentAnswer}
                onChange={(e) => setStudentAnswer(e.target.value)}
                placeholder="Enter the student's answer..."
                rows="4"
              />
            </div>

            <div className="form-group">
              <label>Correct/Expected Answer</label>
              <textarea
                value={correctAnswer}
                onChange={(e) => setCorrectAnswer(e.target.value)}
                placeholder="Enter the correct answer (optional)..."
                rows="4"
              />
            </div>

            <button
              className="btn btn-primary full-width"
              onClick={handleEvaluateAnswer}
              disabled={loading}
            >
              {loading ? <Loader className="spinner" /> : <CheckCircle size={18} />}
              Evaluate Answer
            </button>
          </div>
        )}

        {/* Image Answer Evaluation */}
        {evaluationType === 'image' && (
          <div className="card evaluation-form">
            <h2>Evaluate Image Answer</h2>

            <div className="form-group">
              <label>Upload Answer Image</label>
              <div className="upload-area">
                <input
                  type="file"
                  onChange={handleFileUpload}
                  accept="image/*"
                  id="image-input"
                  className="file-input"
                />
                <label htmlFor="image-input" className="upload-label">
                  <Upload size={32} />
                  <p>Click or drag to upload</p>
                </label>
              </div>
              {uploadedFile && <p className="file-name">Selected: {uploadedFile.name}</p>}
            </div>

            <div className="form-group">
              <label>Question</label>
              <textarea
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Enter the question..."
                rows="3"
              />
            </div>

            <div className="form-group">
              <label>Additional Context (Optional)</label>
              <textarea
                value={answerExplanation}
                onChange={(e) => setAnswerExplanation(e.target.value)}
                placeholder="Add any context or rubric details..."
                rows="3"
              />
            </div>

            <button
              className="btn btn-primary full-width"
              onClick={handleEvaluateImage}
              disabled={loading}
            >
              {loading ? <Loader className="spinner" /> : <CheckCircle size={18} />}
              Evaluate Image
            </button>
          </div>
        )}

        {/* Evaluation Results */}
        {evaluation && (
          <div className="card evaluation-results">
            <h2>Evaluation Results</h2>
            <div className="results-content">
              <MarkdownDisplay content={evaluation} />
            </div>
            <button
              className="btn btn-secondary"
              onClick={() => copyToClipboard(evaluation)}
            >
              Copy Evaluation
            </button>
          </div>
        )}

        {/* Empty State */}
        {!evaluation && (
          <div className="empty-state">
            <CheckCircle size={48} />
            <h3>Ready to Evaluate?</h3>
            <p>Fill in the details above to get AI-powered feedback</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default AnswerEvaluator;
