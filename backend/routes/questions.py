from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from utils import generate_questions, chat_with_llm

router = APIRouter()

class QuestionRequest(BaseModel):
    content: str
    num_questions: int = 5
    difficulty: str = "medium"
    question_type: str = "multiple_choice"  # multiple_choice, short_answer, essay

@router.post("/generate")
async def generate_questions_endpoint(request: QuestionRequest):
    """Generate questions from content"""
    try:
        if not request.content or len(request.content) < 10:
            raise HTTPException(status_code=400, detail="Content too short")
        
        # Validate difficulty
        if request.difficulty not in ["easy", "medium", "hard"]:
            raise HTTPException(status_code=400, detail="Invalid difficulty level")
        
        # Generate questions using LLM
        prompt = f"""Generate {request.num_questions} {request.difficulty} level {request.question_type} questions based on this content.
        
Content:
{request.content[:2000]}

For {request.question_type} format:
- If multiple_choice: include 4 options (A, B, C, D) and indicate correct answer
- If short_answer: provide expected answer keywords
- If essay: provide key points to cover

Format as numbered list with clear structure."""
        
        questions_text = chat_with_llm(prompt)
        
        return {
            "status": "success",
            "questions": questions_text,
            "num_questions": request.num_questions,
            "difficulty": request.difficulty,
            "type": request.question_type
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating questions: {str(e)}")

@router.post("/answer-key")
async def generate_answer_key(request: QuestionRequest):
    """Generate answer key for questions"""
    try:
        prompt = f"""Based on the following content, generate a comprehensive answer key with detailed explanations.

Content:
{request.content[:2000]}

For each point, provide:
1. Key concepts
2. Important details
3. Common student mistakes to watch for
4. Tips for teaching this topic"""
        
        answer_key = chat_with_llm(prompt)
        
        return {
            "status": "success",
            "answer_key": answer_key
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/practice-questions")
async def generate_practice_questions(request: QuestionRequest):
    """Generate practice questions with varied difficulty"""
    try:
        difficulties = ["easy", "medium", "hard"]
        all_questions = {}
        
        for difficulty in difficulties:
            prompt = f"""Generate {request.num_questions // 3} {difficulty} level questions about:

{request.content[:1500]}

Format clearly with difficulty level."""
            
            questions = chat_with_llm(prompt)
            all_questions[difficulty] = questions
        
        return {
            "status": "success",
            "practice_questions": all_questions,
            "total": len(all_questions) * (request.num_questions // 3)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
