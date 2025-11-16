"""Analytics routes: track evaluation scores and generate performance insights."""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Evaluation, Student, User, get_db
from auth import decode_token

router = APIRouter(prefix="/analytics", tags=["analytics"])


def get_current_user_from_header(token: str = None, db: Session = Depends(get_db)):
    """Extract user_id from Bearer token."""
    if not token:
        raise HTTPException(status_code=401, detail="Token required")
    if token.startswith("Bearer "):
        token = token[7:]
    decoded = decode_token(token)
    if not decoded:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.id == decoded["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


class EvaluationCreate(BaseModel):
    student_id: int
    question: str
    student_answer: str
    score: float  # 0-100
    feedback: str = None
    subject: str = None


class StudentAnalytics(BaseModel):
    student_id: int
    student_name: str
    total_evaluations: int
    average_score: float
    highest_score: float
    lowest_score: float
    scores_by_subject: dict = {}
    recent_scores: list = []


@router.post("/evaluate")
async def record_evaluation(
    evaluation: EvaluationCreate,
    token: str = None,
    db: Session = Depends(get_db),
):
    """Record an evaluation/score for a student."""
    try:
        user = get_current_user_from_header(token, db)

        # Verify student belongs to this teacher
        student = (
            db.query(Student)
            .filter(Student.id == evaluation.student_id, Student.teacher_id == user.id)
            .first()
        )
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Create evaluation record
        new_eval = Evaluation(
            user_id=user.id,
            student_id=evaluation.student_id,
            question=evaluation.question,
            student_answer=evaluation.student_answer,
            score=evaluation.score,
            feedback=evaluation.feedback,
            subject=evaluation.subject,
        )
        db.add(new_eval)
        db.commit()
        db.refresh(new_eval)

        return {
            "status": "success",
            "evaluation_id": new_eval.id,
            "score": new_eval.score,
            "created_at": new_eval.created_at.isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error recording evaluation: {str(e)}")


@router.get("/student/{student_id}", response_model=StudentAnalytics)
async def get_student_analytics(student_id: int, token: str = None, db: Session = Depends(get_db)):
    """Get analytics and performance metrics for a specific student."""
    try:
        user = get_current_user_from_header(token, db)

        # Verify student belongs to this teacher
        student = (
            db.query(Student)
            .filter(Student.id == student_id, Student.teacher_id == user.id)
            .first()
        )
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Get all evaluations for this student
        evaluations = (
            db.query(Evaluation)
            .filter(Evaluation.student_id == student_id)
            .order_by(Evaluation.created_at.desc())
            .all()
        )

        if not evaluations:
            return {
                "student_id": student_id,
                "student_name": student.name,
                "total_evaluations": 0,
                "average_score": 0,
                "highest_score": 0,
                "lowest_score": 0,
                "scores_by_subject": {},
                "recent_scores": [],
            }

        # Calculate metrics
        scores = [e.score for e in evaluations]
        total_evaluations = len(evaluations)
        average_score = sum(scores) / total_evaluations if scores else 0
        highest_score = max(scores)
        lowest_score = min(scores)

        # Group scores by subject
        scores_by_subject = {}
        for eval in evaluations:
            subject = eval.subject or "General"
            if subject not in scores_by_subject:
                scores_by_subject[subject] = []
            scores_by_subject[subject].append(eval.score)

        # Average scores per subject
        subject_averages = {
            subject: sum(subj_scores) / len(subj_scores)
            for subject, subj_scores in scores_by_subject.items()
        }

        # Recent 10 scores with metadata
        recent_scores = [
            {
                "score": e.score,
                "subject": e.subject or "General",
                "date": e.created_at.isoformat(),
            }
            for e in evaluations[:10]
        ]

        return {
            "student_id": student_id,
            "student_name": student.name,
            "total_evaluations": total_evaluations,
            "average_score": round(average_score, 2),
            "highest_score": round(highest_score, 2),
            "lowest_score": round(lowest_score, 2),
            "scores_by_subject": subject_averages,
            "recent_scores": recent_scores,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching analytics: {str(e)}")


@router.get("/class-overview")
async def get_class_overview(token: str = None, db: Session = Depends(get_db)):
    """Get overall class analytics: all students and their performance."""
    try:
        user = get_current_user_from_header(token, db)

        # Get all students for this teacher
        students = db.query(Student).filter(Student.teacher_id == user.id).all()

        class_data = []
        for student in students:
            evaluations = db.query(Evaluation).filter(Evaluation.student_id == student.id).all()

            if evaluations:
                scores = [e.score for e in evaluations]
                avg_score = sum(scores) / len(scores)
                class_data.append(
                    {
                        "student_id": student.id,
                        "student_name": student.name,
                        "total_evaluations": len(evaluations),
                        "average_score": round(avg_score, 2),
                    }
                )
            else:
                class_data.append(
                    {
                        "student_id": student.id,
                        "student_name": student.name,
                        "total_evaluations": 0,
                        "average_score": 0,
                    }
                )

        return {
            "total_students": len(students),
            "class_data": class_data,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching class overview: {str(e)}")
