# Teacher Assistant Bot 🎓

An AI-powered web application designed to help teachers with document analysis, question generation, answer evaluation, lesson planning, and intelligent chat support.

## Features ✨

### 1. **Document Analyzer** 📄
- Upload and analyze documents (PDF, TXT, DOC, DOCX, images)
- Get AI-generated explanations of content
- Ask questions about the document
- Extract text from images using OCR

### 2. **Question Generator** 🧠
- Generate questions from educational content
- Multiple question types: Multiple Choice, Short Answer, Essay
- Adjustable difficulty levels (Easy, Medium, Hard)
- Create answer keys automatically
- Generate practice question sets with varied difficulty

### 3. **Answer Evaluator** ✅
- Evaluate student text answers with detailed feedback
- Support for image-based answers (handwritten)
- Rubric-based evaluation
- Bulk evaluation for multiple answers
- Score and feedback generation

### 4. **Lesson Planner** 📅
- Create comprehensive lesson plans
- Generate week-by-week breakdowns
- Create daily class schedules
- Generate assessment plans aligned with lessons
- Get resource recommendations

### 5. **Chat Bot** 💬
- General chat with AI for teaching advice
- Teaching tips and strategies
- Curriculum guidance
- Classroom management advice
- Assessment and grading help
- Differentiation strategies
- Optional web search integration

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **API**: Hugging Face Inference API (free models)
- **Document Processing**: PyPDF2, Pillow
- **Server**: Uvicorn

### Frontend
- **Framework**: React 18
- **Styling**: CSS3 with modern gradients and animations
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Routing**: React Router v6

### AI Models (Free Tier - Hugging Face)
- **Text Generation**: Mistral-7B-Instruct (for questions, chat, lesson planning)
- **Question Answering**: RoBERTa-base-SQuAD2 (for answer evaluation)
- **Text Classification**: DistilBERT (for content analysis)

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- Hugging Face API Key (free from https://huggingface.co)

### Backend Setup

1. Navigate to backend folder:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Copy the .env.example to .env
copy .env.example .env

# Edit .env and add your Hugging Face API key
HF_API_KEY=your_actual_api_key_here
```

5. Run the backend server:
```bash
python main.py
```

Backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend folder:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm start
```

Frontend will run on `http://localhost:3000`

## Getting Hugging Face API Key

1. Go to https://huggingface.co
2. Sign up for a free account
3. Go to Settings > Access Tokens
4. Create a new token with 'read' access
5. Copy the token and add it to `.env` file in backend

## Project Structure

```
Teacher_Assistant/
├── backend/
│   ├── main.py                 # Main FastAPI application
│   ├── config.py               # Configuration and settings
│   ├── utils.py                # Utility functions for AI integration
│   ├── requirements.txt         # Python dependencies
│   ├── .env                     # Environment variables
│   └── routes/
│       ├── document.py          # Document upload & analysis endpoints
│       ├── questions.py         # Question generation endpoints
│       ├── evaluation.py        # Answer evaluation endpoints
│       ├── lesson_plan.py       # Lesson planning endpoints
│       └── chat.py              # Chat & advice endpoints
│
└── frontend/
    ├── package.json             # Node dependencies
    ├── public/
    │   ├── index.html           # HTML template
    │   └── index.css            # Global styles
    └── src/
        ├── App.js               # Main React component
        ├── App.css              # App styles
        ├── index.js             # React entry point
        ├── index.css            # Global CSS
        ├── api/
        │   └── index.js         # API client (Axios)
        ├── components/
        │   ├── Navbar.js        # Navigation bar
        │   ├── Sidebar.js       # Sidebar navigation
        │   └── *.css            # Component styles
        └── pages/
            ├── Dashboard.js     # Home dashboard
            ├── DocumentAnalyzer.js
            ├── QuestionGenerator.js
            ├── AnswerEvaluator.js
            ├── LessonPlanner.js
            ├── ChatBot.js
            └── *.css            # Page styles
```

## API Endpoints

### Document APIs
- `POST /api/document/upload` - Upload a document
- `GET /api/document/list` - List all uploaded documents
- `GET /api/document/explain/{filename}` - Get explanation of a document

### Question APIs
- `POST /api/questions/generate` - Generate questions
- `POST /api/questions/answer-key` - Generate answer key
- `POST /api/questions/practice-questions` - Generate practice questions

### Evaluation APIs
- `POST /api/evaluation/evaluate-answer` - Evaluate text answer
- `POST /api/evaluation/evaluate-image` - Evaluate image answer
- `POST /api/evaluation/rubric-based` - Rubric-based evaluation
- `POST /api/evaluation/bulk-evaluate` - Bulk evaluate answers

### Lesson Plan APIs
- `POST /api/lesson-plan/create` - Create full lesson plan
- `POST /api/lesson-plan/week-plan` - Create week plan
- `POST /api/lesson-plan/daily-schedule` - Create daily schedule
- `POST /api/lesson-plan/assessment-plan` - Create assessment plan
- `POST /api/lesson-plan/resource-recommendations` - Get resources

### Chat APIs
- `POST /api/chat/send` - Send chat message
- `POST /api/chat/teaching-advice` - Get teaching advice
- `POST /api/chat/curriculum-help` - Get curriculum guidance
- `POST /api/chat/classroom-management` - Get classroom management advice
- `POST /api/chat/assessment-help` - Get assessment help
- `POST /api/chat/differentiation-strategies` - Get differentiation strategies

## Usage Guide

### 1. Document Analysis
1. Go to "Document Analyzer"
2. Upload a PDF, image, or text file
3. View the document preview
4. Click "Get Explanation" for AI-generated summary
5. Ask questions about the content in the chat box

### 2. Generate Questions
1. Go to "Question Generator"
2. Paste content or topic text
3. Choose number of questions, difficulty, and type
4. Click "Generate Questions" to create questions
5. Use "Generate Answer Key" for model answers
6. Copy results to use in your lessons

### 3. Evaluate Answers
1. Go to "Answer Evaluator"
2. Choose evaluation type (Text or Image)
3. For text: Enter question and student answer
4. For image: Upload image of handwritten answer
5. Get detailed feedback and scoring

### 4. Create Lesson Plans
1. Go to "Lesson Planner"
2. Enter chapter name and topics
3. Choose class level and duration
4. Click the type of plan you need:
   - Full Lesson Plan (comprehensive overview)
   - Week Plan (detailed weekly breakdown)
   - Daily Schedule (hour-by-hour class plan)
   - Assessment Plan (evaluation strategy)
   - Resources (recommended materials)

### 5. Chat with AI
1. Go to "Chat Bot"
2. Select chat mode (General, Teaching, Curriculum, etc.)
3. Type your question or topic
4. Optional: Enable web search for current information
5. Use quick action buttons for common questions

## Features in Detail

### Advanced Settings
- **Difficulty Levels**: Easy, Medium, Hard
- **Question Types**: Multiple Choice, Short Answer, Essay
- **Class Levels**: Elementary, Middle School, High School, College
- **Assessment Types**: Formative, Summative

### Supported File Formats
- Documents: PDF, TXT, DOC, DOCX
- Images: PNG, JPG, JPEG

### AI Capabilities
- Natural language understanding
- Content summarization
- Question generation with varied difficulty
- Answer evaluation with rubric support
- Lesson plan creation with timeline
- Teaching advice and guidance

## Customization

### Changing AI Models
Edit `backend/config.py`:
```python
MODELS = {
    "text_generation": "your_preferred_model",
    "question_answering": "your_preferred_model",
    "text_classification": "your_preferred_model",
}
```

### Styling
- Global styles: `frontend/src/index.css`
- Component styles: Individual `.css` files in components/pages folders
- Update color scheme in any `.css` file

## Troubleshooting

### Issue: "API Key not working"
- Verify your Hugging Face API key is correct
- Check it's in the `.env` file with exact format
- Restart the backend server after updating `.env`

### Issue: "Connection refused"
- Ensure backend is running on port 8000
- Check if frontend `.env` has correct API URL
- Clear browser cache and restart

### Issue: "File upload failing"
- Check file size is under 50MB
- Verify file format is supported
- Check uploads/ folder has write permissions

### Issue: "Slow responses"
- Hugging Face free tier may have rate limiting
- Wait a moment and try again
- Consider upgrading to paid tier for faster responses

## Deployment

### Deploy Backend (Heroku)
1. Install Heroku CLI
2. `heroku create your-app-name`
3. `git push heroku main`

### Deploy Frontend (Vercel)
1. `npm run build`
2. Deploy `build/` folder to Vercel or Netlify

## Browser Support
- Chrome (recommended)
- Firefox
- Safari
- Edge

## License
MIT

## Support
For issues and questions, please create an issue in the repository.

## Future Enhancements
- Database integration for saving lessons and evaluations
- User authentication and profiles
- Real-time collaboration features
- Mobile app version
- Advanced analytics dashboard
- Integration with learning management systems (LMS)
- Video content support
- Automated grading system
- Parent communication portal

---

**Happy Teaching! 🎓✨**
