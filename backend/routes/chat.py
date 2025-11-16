from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import json
from utils import chat_with_llm
from utils import chat_with_llm, semantic_search
import requests

router = APIRouter()

class ChatMessage(BaseModel):
    message: str
    context: Optional[str] = None
    enable_search: bool = False

class TeachingAdviceRequest(BaseModel):
    topic: str
    challenge: str
    class_level: str = "high school"

class CurriculumHelpRequest(BaseModel):
    subject: str
    standard: str
    question: str

class ClassroomManagementRequest(BaseModel):
    situation: str
    context: Optional[str] = None
    grade_level: str = "high school"

class AssessmentHelpRequest(BaseModel):
    question: str

class DifferentiationRequest(BaseModel):
    content: str
    class_composition: str = "mixed abilities"

class ChatHistory(BaseModel):
    messages: List[dict]

@router.post("/send")
async def send_message(request: ChatMessage):
    """Send a message to the LLM"""
    try:
        search_results = ""
        
        # If search is enabled, perform web search
        if request.enable_search:
            # First try semantic search against local vector DB
            search_hits = semantic_search(request.message, top_k=3)
            if search_hits:
                combined = '\n\n'.join([f"Source: {h['filename']}\n{h['text'][:1000]}" for h in search_hits])
                prompt = f"""Answer the user's question using your knowledge and the following document excerpts (from uploaded documents):

Document Excerpts:
{combined}

User Question: {request.message}

Provide a comprehensive answer combining both your knowledge and the document excerpts. Cite sources when relevant."""
            else:
                # fallback to web search placeholder
                search_results = await search_google(request.message)
                if search_results:
                    prompt = f"""Answer the user's question using your knowledge and the following search results:

Search Results:
{search_results}

User Question: {request.message}

Provide a comprehensive answer combining both your knowledge and the search results. Cite sources when relevant."""
                else:
                    prompt = request.message
        else:
            if request.context:
                prompt = f"{request.context}\n\nUser: {request.message}"
            else:
                prompt = request.message
        
        response = chat_with_llm(prompt)
        
        return {
            "status": "success",
            "message": request.message,
            "response": response,
            "search_enabled": request.enable_search
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def search_google(query: str) -> str:
    """Perform a web search"""
    try:
        # Using a free search API - you can replace with your preferred service
        # This is a placeholder - implement actual search if needed
        search_prompt = f"Search results for: {query}"
        return search_prompt
    except Exception as e:
        return ""

@router.post("/debug-echo")
async def debug_echo(request: ChatMessage):
    """Simple echo endpoint for end-to-end UI tests"""
    try:
        return {
            "status": "success",
            "response": f"Echo: {request.message}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/teaching-advice")
async def get_teaching_advice(request: TeachingAdviceRequest):
    """Get teaching advice for a specific challenge"""
    try:
        prompt = f"""I'm a {request.class_level} teacher and need advice:

Topic: {request.topic}
Challenge: {request.challenge}

Please provide:
1. Root cause analysis
2. Specific strategies to address this
3. Activities or techniques to try
4. How to measure effectiveness
5. Resources that might help
6. Tips from experienced teachers
7. How to adapt for different learning styles
8. Prevention strategies for future"""
        
        advice = chat_with_llm(prompt)
        
        return {
            "status": "success",
            "response": advice
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/curriculum-help")
async def get_curriculum_help(request: CurriculumHelpRequest):
    """Get help with curriculum and standards"""
    try:
        prompt = f"""Help me understand curriculum standards:

Subject: {request.subject}
Standard: {request.standard}
Question: {request.question}

Provide:
1. Clear explanation of the standard
2. Learning outcomes
3. How to assess student mastery
4. Teaching strategies
5. Common misconceptions
6. Real-world applications
7. Cross-curricular connections
8. Differentiation strategies"""
        
        help_text = chat_with_llm(prompt)
        
        return {
            "status": "success",
            "response": help_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/classroom-management")
async def get_classroom_management_advice(request: ClassroomManagementRequest):
    """Get advice on classroom management"""
    try:
        prompt = f"""I need classroom management advice for a {request.grade_level} class:

Situation: {request.situation}
{f'Context: {request.context}' if request.context else ''}

Please provide:
1. What might be causing this behavior
2. Immediate strategies to try
3. Long-term prevention strategies
4. How to address root causes
5. Communication strategies with students
6. Involving parents if needed
7. Building positive classroom culture
8. Resources and support available"""
        
        advice = chat_with_llm(prompt)
        
        return {
            "status": "success",
            "response": advice
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/assessment-help")
async def get_assessment_help(request: AssessmentHelpRequest):
    """Get help with assessment and grading"""
    try:
        prompt = f"""I need help with assessment:

Question: {request.question}

Provide:
1. Best practices for assessment
2. How to score objectively
3. Common grading pitfalls to avoid
4. How to give meaningful feedback
5. Accommodations for different learners
6. How to use results to improve instruction
7. Tools and resources
8. Examples of strong vs weak responses"""
        
        help_text = chat_with_llm(prompt)
        
        return {
            "status": "success",
            "response": help_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/differentiation-strategies")
async def get_differentiation_strategies(request: DifferentiationRequest):
    """Get strategies for differentiating instruction"""
    try:
        prompt = f"""Help me differentiate instruction:

Content: {request.content}
Class Composition: {request.class_composition}

Provide differentiation strategies for:
1. Advanced learners (enrichment activities)
2. On-level learners (core instruction)
3. Struggling learners (support strategies)
4. English language learners
5. Students with disabilities
6. Different learning styles
7. Pacing variations
8. Assessment modifications

Include specific activities and materials."""
        
        strategies = chat_with_llm(prompt)
        
        return {
            "status": "success",
            "response": strategies
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/history")
async def get_chat_history(session_id: str):
    """Retrieve chat history for a session"""
    try:
        # This would connect to a database in production
        return {
            "status": "success",
            "session_id": session_id,
            "message": "Chat history feature - connect to database for production"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/clear-history")
async def clear_chat_history(session_id: str):
    """Clear chat history for a session"""
    try:
        return {
            "status": "success",
            "message": "Chat history cleared"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
