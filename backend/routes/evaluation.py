from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
import shutil
from config import UPLOAD_DIR
from utils import extract_text_from_image, chat_with_llm

router = APIRouter()

class EvaluationRequest(BaseModel):
    question: str
    student_answer: str
    correct_answer: str
    rubric: Optional[str] = None

@router.post("/evaluate-answer")
async def evaluate_answer(request: EvaluationRequest):
    """Evaluate student answer"""
    try:
        rubric_text = f"\n\nRubric to follow:\n{request.rubric}" if request.rubric else ""
        
        prompt = f"""Evaluate the following student answer on a scale of 0-100 and provide detailed feedback.

Question: {request.question}

Student's Answer: {request.student_answer}

Expected/Model Answer: {request.correct_answer}
{rubric_text}

Provide your evaluation in the following format:
1. Score: [0-100]
2. Strengths: [What the student did well]
3. Areas for Improvement: [What needs work]
4. Correct Aspects: [What was correct]
5. Missing Concepts: [What was left out]
6. Feedback: [Detailed constructive feedback]
7. Suggested Resources: [Recommendations to improve]"""
        
        evaluation = chat_with_llm(prompt)
        
        return {
            "status": "success",
            "evaluation": evaluation,
            "question": request.question
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/evaluate-image")
async def evaluate_image(
    file: UploadFile = File(...),
    question: str = "",
    answer_explanation: str = ""
):
    """Evaluate answer from uploaded image"""
    try:
        # Save temporary file
        file_path = os.path.join(UPLOAD_DIR, f"temp_{file.filename}")
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract text from image
        extracted_text = extract_text_from_image(file_path)
        
        # Evaluate the extracted answer
        prompt = f"""The following is a student's handwritten/photographed answer to a question.

Question: {question}

Extracted Answer Text:
{extracted_text}

{answer_explanation if answer_explanation else 'Please evaluate this answer based on accuracy and completeness.'}

Provide:
1. Transcription confirmation (is the text correct?)
2. Accuracy assessment
3. Completeness check
4. Score (0-100)
5. Feedback and suggestions"""
        
        evaluation = chat_with_llm(prompt)
        
        # Clean up temp file
        if os.path.exists(file_path):
            os.remove(file_path)
        
        return {
            "status": "success",
            "extracted_text": extracted_text,
            "evaluation": evaluation,
            "filename": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating image: {str(e)}")

@router.post("/rubric-based")
async def rubric_based_evaluation(
    question: str,
    student_answer: str,
    rubric_criteria: dict  # {criterion: {max_points: int, description: str}}
):
    """Evaluate based on specific rubric"""
    try:
        rubric_text = "Rubric:\n"
        total_points = 0
        for criterion, details in rubric_criteria.items():
            rubric_text += f"\n{criterion}: {details['max_points']} points\n{details['description']}"
            total_points += details['max_points']
        
        prompt = f"""Using the following rubric, evaluate the student's answer:

Question: {question}

Student Answer: {student_answer}

{rubric_text}

Total Points: {total_points}

Provide:
1. Points for each criterion
2. Total score
3. Justification for each score
4. Strengths
5. Areas for improvement
6. Specific feedback"""
        
        evaluation = chat_with_llm(prompt)
        
        return {
            "status": "success",
            "evaluation": evaluation,
            "total_points": total_points,
            "criteria": list(rubric_criteria.keys())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/bulk-evaluate")
async def bulk_evaluate_answers(
    evaluations: list  # List of {question, student_answer, correct_answer}
):
    """Evaluate multiple answers"""
    try:
        results = []
        for item in evaluations:
            prompt = f"""Quick evaluation of student answer:
Question: {item['question']}
Answer: {item['student_answer']}
Expected: {item['correct_answer']}

Score (0-100) and brief feedback."""
            
            eval_result = chat_with_llm(prompt)
            results.append({
                "question": item['question'],
                "evaluation": eval_result
            })
        
        return {
            "status": "success",
            "evaluations": results,
            "total_evaluated": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
