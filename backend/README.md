# Teacher Assistant Bot - Backend

FastAPI backend for the Teacher Assistant Bot application.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/Scripts/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
copy .env.example .env
# Edit .env and add your Hugging Face API key
```

4. Run server:
```bash
python main.py
```

Server runs on http://localhost:8000

## API Documentation

Once running, view interactive API docs at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Configuration

Edit `config.py` to:
- Change AI models
- Adjust upload file size limits
- Modify allowed file types
- Update Hugging Face settings

## Files

- `main.py` - FastAPI application entry point
- `config.py` - Configuration settings
- `utils.py` - Utility functions for AI integration
- `routes/` - API endpoint implementations
  - `document.py` - Document handling
  - `questions.py` - Question generation
  - `evaluation.py` - Answer evaluation
  - `lesson_plan.py` - Lesson planning
  - `chat.py` - Chat and advice endpoints

## Hugging Face Models

The application uses free Hugging Face models:
- Mistral-7B for text generation
- RoBERTa for question answering
- DistilBERT for text classification

Get API key at: https://huggingface.co/settings/tokens
