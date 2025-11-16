from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
from dotenv import load_dotenv
from routes import document, questions, evaluation, lesson_plan, chat, auth, students, analytics

# Load environment variables
load_dotenv()

app = FastAPI(title="Teacher Assistant Bot", version="1.0.0")


@app.on_event("startup")
def ensure_test_user():
    """Ensure a default test user exists (username: Testuser, password: 1234).

    This makes it convenient to sign in during development. The password is
    hashed using the project's hashing utility.
    """
    try:
        from models import SessionLocal, User
        from auth import hash_password

        db = SessionLocal()
        existing = db.query(User).filter(User.username == "Testuser").first()
        if not existing:
            test_user = User(
                username="Testuser",
                email="testuser@example.com",
                hashed_password=hash_password("1234"),
                full_name="Test User",
            )
            db.add(test_user)
            db.commit()
            print("Created default Testuser (username=Testuser, password=1234)")
        db.close()
    except Exception as e:
        # Startup should not crash if DB or hashing unavailable; log for debugging
        print(f"Warning: could not ensure Testuser exists: {e}")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(document.router, prefix="/api/document", tags=["Document"])
app.include_router(questions.router, prefix="/api/questions", tags=["Questions"])
app.include_router(evaluation.router, prefix="/api/evaluation", tags=["Evaluation"])
app.include_router(lesson_plan.router, prefix="/api/lesson-plan", tags=["Lesson Plan"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(auth.router, tags=["Auth"])
app.include_router(students.router, prefix="/api/students", tags=["Students"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])

@app.get("/")
def read_root():
    return {
        "message": "Teacher Assistant Bot API",
        "version": "1.0.0",
        "endpoints": {
            "document": "/api/document",
            "questions": "/api/questions",
            "evaluation": "/api/evaluation",
            "lesson_plan": "/api/lesson-plan",
            "chat": "/api/chat"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
