"""Student management routes: add, list, get, update, delete students."""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import Student, User, get_db
from auth import decode_token

router = APIRouter(prefix="/students", tags=["students"])


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


class StudentCreate(BaseModel):
    name: str
    email: str = None
    grade_level: str = None


class StudentResponse(BaseModel):
    id: int
    name: str
    email: str = None
    grade_level: str = None
    created_at: str

    class Config:
        from_attributes = True


@router.post("/add", response_model=StudentResponse)
async def add_student(
    student: StudentCreate,
    token: str = None,
    db: Session = Depends(get_db),
):
    """Add a new student for the logged-in teacher."""
    try:
        user = get_current_user_from_header(token, db)

        new_student = Student(
            teacher_id=user.id,
            name=student.name,
            email=student.email,
            grade_level=student.grade_level,
        )
        db.add(new_student)
        db.commit()
        db.refresh(new_student)

        return {
            "id": new_student.id,
            "name": new_student.name,
            "email": new_student.email,
            "grade_level": new_student.grade_level,
            "created_at": new_student.created_at.isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding student: {str(e)}")


@router.get("/list", response_model=list[StudentResponse])
async def list_students(token: str = None, db: Session = Depends(get_db)):
    """List all students for the logged-in teacher."""
    try:
        user = get_current_user_from_header(token, db)

        students = db.query(Student).filter(Student.teacher_id == user.id).all()

        return [
            {
                "id": s.id,
                "name": s.name,
                "email": s.email,
                "grade_level": s.grade_level,
                "created_at": s.created_at.isoformat(),
            }
            for s in students
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing students: {str(e)}")


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(student_id: int, token: str = None, db: Session = Depends(get_db)):
    """Get details of a specific student."""
    try:
        user = get_current_user_from_header(token, db)

        student = (
            db.query(Student)
            .filter(Student.id == student_id, Student.teacher_id == user.id)
            .first()
        )
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        return {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "grade_level": student.grade_level,
            "created_at": student.created_at.isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching student: {str(e)}")


@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: int,
    student_data: StudentCreate,
    token: str = None,
    db: Session = Depends(get_db),
):
    """Update student details."""
    try:
        user = get_current_user_from_header(token, db)

        student = (
            db.query(Student)
            .filter(Student.id == student_id, Student.teacher_id == user.id)
            .first()
        )
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        student.name = student_data.name
        student.email = student_data.email or student.email
        student.grade_level = student_data.grade_level or student.grade_level

        db.commit()
        db.refresh(student)

        return {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "grade_level": student.grade_level,
            "created_at": student.created_at.isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating student: {str(e)}")


@router.delete("/{student_id}")
async def delete_student(student_id: int, token: str = None, db: Session = Depends(get_db)):
    """Delete a student."""
    try:
        user = get_current_user_from_header(token, db)

        student = (
            db.query(Student)
            .filter(Student.id == student_id, Student.teacher_id == user.id)
            .first()
        )
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        db.delete(student)
        db.commit()

        return {"status": "success", "message": "Student deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting student: {str(e)}")
