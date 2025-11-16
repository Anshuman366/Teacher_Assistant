from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from utils import chat_with_llm

router = APIRouter()

class LessonPlanRequest(BaseModel):
    chapter_name: str
    topics: List[str]
    lectures_per_week: int
    total_weeks: int
    class_level: str = "high school"  # high school, college, etc.
    learning_style: Optional[str] = None

class LessonPlanResponse(BaseModel):
    chapter_name: str
    lesson_plan: str
    timeline: str
    resources: List[str]
    assessments: str

@router.post("/create")
async def create_lesson_plan(request: LessonPlanRequest):
    """Create a detailed lesson plan"""
    try:
        topics_str = ", ".join(request.topics)
        
        prompt = f"""Create a comprehensive lesson plan with the following requirements:

Chapter: {request.chapter_name}
Topics: {topics_str}
Class Level: {request.class_level}
Duration: {request.total_weeks} weeks
Lectures per week: {request.lectures_per_week}
Total lectures: {request.total_weeks * request.lectures_per_week}

For each topic, provide a week-by-week breakdown including:
1. Learning Objectives
2. Key Concepts
3. Teaching Methods/Activities
4. Time Allocation (in minutes)
5. Resources Needed
6. Assessment Methods
7. Homework/Assignments
8. Discussion Points

Format as a structured timeline that spreads content across {request.total_weeks} weeks.

the data should be presented in a markdown clear and organized manner, suitable for direct implementation by educators.

"""
        
        lesson_plan = chat_with_llm(prompt)
        
        return {
            "status": "success",
            "lesson_plan": lesson_plan,
            "chapter": request.chapter_name,
            "total_weeks": request.total_weeks,
            "lectures_total": request.total_weeks * request.lectures_per_week
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/week-plan")
async def create_week_plan(
    chapter_name: str,
    week_number: int,
    topics: List[str],
    lectures_in_week: int
):
    """Create a detailed plan for a specific week"""
    try:
        topics_str = ", ".join(topics)
        
        prompt = f"""Create a detailed week-by-week lesson plan for Week {week_number}:

Chapter: {chapter_name}
Topics for this week: {topics_str}
Number of lectures: {lectures_in_week}
Minutes per lecture: Assume 50 minutes per lecture

For each lecture, provide:
1. Lecture title
2. Duration breakdown (introduction, main content, activities, conclusion)
3. Key learning outcomes
4. Interactive activities
5. Resources- provide link from web
6. Pre-lecture preparations for students
7. Post-lecture assignments
8. Assessment activities

Create a detailed, hour-by-hour or minute-by-minute breakdown in markdown format."""
        
        week_plan = chat_with_llm(prompt)
        
        return {
            "status": "success",
            "week_number": week_number,
            "week_plan": week_plan,
            "lectures": lectures_in_week
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/daily-schedule")
async def create_daily_schedule(
    chapter_name: str,
    date: str,
    topics_to_cover: List[str],
    duration_minutes: int = 50
):
    """Create a detailed daily schedule for a single class"""
    try:
        topics_str = ", ".join(topics_to_cover)
        
        prompt = f"""Create a detailed class schedule for today:

Date: {date}
Chapter: {chapter_name}
Topics: {topics_str}
Class Duration: {duration_minutes} minutes

Provide a minute-by-minute breakdown:
- Opening (2-3 min): Hook/recap
- Introduction (5 min): Objectives and agenda
- Content Delivery (20-25 min): Main teaching
- Interactive Activity (15-20 min): Hands-on activity/discussion
- Assessment (5 min): Check for understanding
- Closing (3-5 min): Summary and preview

Include:
1. Materials needed
2. Questions to ask students
3. Common misconceptions to address
4. Accessibility considerations
5. Homework preview"""
        
        schedule = chat_with_llm(prompt)
        
        return {
            "status": "success",
            "date": date,
            "duration": duration_minutes,
            "schedule": schedule
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/assessment-plan")
async def create_assessment_plan(
    chapter_name: str,
    topics: List[str],
    total_weeks: int,
    assessment_types: List[str] = ["formative", "summative"]
):
    """Create assessment plan aligned with lesson plan"""
    try:
        topics_str = ", ".join(topics)
        
        prompt = f"""Create a comprehensive assessment plan:

Chapter: {chapter_name}
Topics: {topics_str}
Duration: {total_weeks} weeks
Assessment Types: {", ".join(assessment_types)}

Provide:
1. Formative Assessment Plan (weekly checks, quizzes, discussions)
2. Summative Assessment Plan (tests, projects, presentations)
3. Week-by-week assessment timeline
4. Assessment tools (rubrics, checklists, criteria)
5. Rubric samples for major assessments
6. How to use assessments to inform instruction

For each week, specify:
- Type of assessment
- What will be assessed
- When (which lecture/day)
- How it connects to learning objectives
- Feedback timeline"""
        
        assessment_plan = chat_with_llm(prompt)
        
        return {
            "status": "success",
            "chapter": chapter_name,
            "assessment_plan": assessment_plan,
            "assessment_types": assessment_types
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/resource-recommendations")
async def get_resource_recommendations(
    chapter_name: str,
    topics: List[str],
    class_level: str
):
    """Get recommended resources for the lesson plan"""
    try:
        topics_str = ", ".join(topics)
        
        prompt = f"""Recommend teaching resources for:

Chapter: {chapter_name}
Topics: {topics_str}
Class Level: {class_level}

Provide recommendations for:
1. Textbook chapters and pages
2. Video resources (Khan Academy, YouTube, etc.)
3. Interactive simulations and tools
4. Hands-on materials/experiments
5. Real-world applications and examples
6. Discussion starters
7. Assessment tools
8. Accessibility resources
9. Extensions for advanced students
10. Support resources for struggling students"""
        
        resources = chat_with_llm(prompt)
        
        return {
            "status": "success",
            "resources": resources,
            "chapter": chapter_name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
