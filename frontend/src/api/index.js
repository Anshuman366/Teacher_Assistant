import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

// Document APIs
export const uploadDocument = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/document/upload', formData);
};

export const getDocuments = () => {
  return api.get('/document/list');
};

export const explainDocument = (filename) => {
  return api.get(`/document/explain/${filename}`);
};

export const askDocument = (filename, data) => {
  return api.post(`/document/ask/${filename}`, data);
};

// Question APIs
export const generateQuestions = (data) => {
  return api.post('/questions/generate', data);
};

export const generateAnswerKey = (data) => {
  return api.post('/questions/answer-key', data);
};

export const generatePracticeQuestions = (data) => {
  return api.post('/questions/practice-questions', data);
};

// Evaluation APIs
export const evaluateAnswer = (data) => {
  return api.post('/evaluation/evaluate-answer', data);
};

export const evaluateImage = (file, question, explanation) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('question', question);
  formData.append('answer_explanation', explanation);
  return api.post('/evaluation/evaluate-image', formData);
};

export const rubricBasedEvaluation = (data) => {
  return api.post('/evaluation/rubric-based', data);
};

export const bulkEvaluateAnswers = (data) => {
  return api.post('/evaluation/bulk-evaluate', { evaluations: data });
};

// Lesson Plan APIs
export const createLessonPlan = (data) => {
  return api.post('/lesson-plan/create', data);
};

export const createWeekPlan = (data) => {
  return api.post('/lesson-plan/week-plan', data);
};

export const createDailySchedule = (data) => {
  return api.post('/lesson-plan/daily-schedule', data);
};

export const createAssessmentPlan = (data) => {
  return api.post('/lesson-plan/assessment-plan', data);
};

export const getResourceRecommendations = (data) => {
  return api.post('/lesson-plan/resource-recommendations', data);
};

// Chat APIs
export const sendChatMessage = (data) => {
  return api.post('/chat/send', data);
};

export const getTeachingAdvice = (data) => {
  return api.post('/chat/teaching-advice', data);
};

export const getCurriculumHelp = (data) => {
  return api.post('/chat/curriculum-help', data);
};

export const getClassroomManagementAdvice = (data) => {
  return api.post('/chat/classroom-management', data);
};

export const getAssessmentHelp = (data) => {
  return api.post('/chat/assessment-help', data);
};

export const getDifferentiationStrategies = (data) => {
  return api.post('/chat/differentiation-strategies', data);
};

export default api;
