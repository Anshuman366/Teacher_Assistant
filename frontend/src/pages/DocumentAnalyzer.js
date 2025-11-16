import React, { useState } from 'react';
import { Upload, FileText, Loader } from 'lucide-react';
import { uploadDocument, explainDocument, askDocument } from '../api';
import MarkdownDisplay from '../components/MarkdownDisplay';
import './DocumentAnalyzer.css';

function DocumentAnalyzer() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [explanation, setExplanation] = useState('');
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState('');
  const [showExplanation, setShowExplanation] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    
    setLoading(true);
    try {
      const result = await uploadDocument(file);
      setUploadedFile(result.data);
      setExplanation('');
      setQuestion('');
      setResponse('');
    } catch (error) {
      console.error('Upload error:', error);
      alert('Error uploading file');
    } finally {
      setLoading(false);
    }
  };

  const handleGetExplanation = async () => {
    if (!uploadedFile) return;
    
    setLoading(true);
    try {
      const result = await explainDocument(uploadedFile.filename);
      setExplanation(result.data.explanation);
      setShowExplanation(true);
    } catch (error) {
      console.error('Error getting explanation:', error);
      alert('Error getting explanation');
    } finally {
      setLoading(false);
    }
  };

  const handleAskQuestion = async () => {
    if (!question || !uploadedFile) return;

    setLoading(true);
    try {
      const res = await askDocument(uploadedFile.filename, { question });
      setResponse(res.data.response);
    } catch (error) {
      console.error('Error asking question:', error);
      alert('Error processing question');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="document-analyzer">
      <h1 className="page-title">📄 Document Analyzer</h1>
      <p className="page-description">
        Upload documents or images to get explanations, ask questions, and more
      </p>

      <div className="analyzer-container">
        {/* Upload Section */}
        <div className="card upload-section">
          <h2>Upload Document</h2>
          <div className="upload-area">
            <input
              type="file"
              onChange={handleFileChange}
              accept=".pdf,.txt,.doc,.docx,.png,.jpg,.jpeg"
              className="file-input"
              id="file-input"
            />
            <label htmlFor="file-input" className="upload-label">
              <Upload size={32} />
              <p>Drag and drop or click to select file</p>
              <span className="file-types">PDF, TXT, DOC, DOCX, PNG, JPG</span>
            </label>
          </div>
          
          {file && <p className="file-name">Selected: {file.name}</p>}
          
          <button 
            className="btn btn-primary"
            onClick={handleUpload}
            disabled={!file || loading}
          >
            {loading ? <Loader className="spinner" /> : 'Upload Document'}
          </button>
        </div>

        {/* Content Display */}
        {uploadedFile && (
          <div className="content-display">
            {/* Document Info */}
            <div className="card doc-info">
              <h2>Document Info</h2>
              <div className="info-item">
                <span className="label">Filename:</span>
                <span className="value">{uploadedFile.filename}</span>
              </div>
              <div className="info-item">
                <span className="label">Type:</span>
                <span className="value badge badge-success">{uploadedFile.file_type}</span>
              </div>
              <div className="info-item">
                <span className="label">Size:</span>
                <span className="value">{(uploadedFile.size / 1024).toFixed(2)} KB</span>
              </div>
            </div>

            {/* Preview */}
            <div className="card preview-section">
              <h2>Content Preview</h2>
              <div className="content-preview">
                {uploadedFile.content}...
              </div>
            </div>

            {/* Explanation */}
            {!showExplanation && (
              <button 
                className="btn btn-primary full-width"
                onClick={handleGetExplanation}
                disabled={loading}
              >
                {loading ? <Loader className="spinner" /> : 'Get Explanation'}
              </button>
            )}

            {showExplanation && explanation && (
              <div className="card explanation-section">
                <h2>Explanation</h2>
                <div className="explanation-content">
                  <MarkdownDisplay content={explanation} />
                </div>
              </div>
            )}

            {/* Ask Question */}
            <div className="card question-section">
              <h2>Ask Questions About the Document</h2>
              <div className="input-group">
                <textarea
                  placeholder="Ask any question about this document..."
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  rows="4"
                />
              </div>
              <button 
                className="btn btn-primary"
                onClick={handleAskQuestion}
                disabled={!question || loading}
              >
                {loading ? <Loader className="spinner" /> : 'Ask Question'}
              </button>

              {response && (
                <div className="response-box">
                  <h3>Answer:</h3>
                  <MarkdownDisplay content={response} />
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default DocumentAnalyzer;
