@echo off
echo.
echo ============================================================
echo TEACHER ASSISTANT BOT - QUICK START
echo ============================================================
echo.

REM Activate virtual environment if it exists
if exist "backend\venv\Scripts\activate.bat" (
    echo 🔌 Activating virtual environment...
    call backend\venv\Scripts\activate.bat
    echo ✓ Virtual environment activated
) else (
    echo ⚠️  Virtual environment not found
    echo Creating virtual environment...
    cd backend
    python -m venv venv
    call venv\Scripts\activate.bat
    cd ..
    echo ✓ Virtual environment created
    
    echo Installing dependencies...
    pip install -q -r backend\requirements.txt
    echo ✓ Dependencies installed
)

echo.
echo 🔍 Running diagnostic...
python check.py

echo.
echo ============================================================
echo 📝 TO START THE APPLICATION:
echo ============================================================
echo.
echo Terminal 1 - Backend:
echo   cd backend
echo   python main.py
echo.
echo Terminal 2 - Frontend:
echo   cd frontend
echo   npm start
echo.
echo Then visit: http://localhost:3000
echo.
pause
