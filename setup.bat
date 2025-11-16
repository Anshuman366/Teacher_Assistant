@echo off
REM Teacher Assistant Bot - Quick Start Script for Windows

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   Teacher Assistant Bot - Setup Script                ║
echo ║   AI-Powered Teaching Tool                            ║
echo ╚════════════════════════════════════════════════════════╝
echo.

set HF_API_KEY=

echo Please enter your Hugging Face API Key:
set /p HF_API_KEY="API Key: "

if "%HF_API_KEY%"=="" (
    echo Error: API Key is required!
    pause
    exit /b 1
)

echo.
echo [1/4] Creating backend virtual environment...
cd backend
python -m venv venv
if %errorlevel% neq 0 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/4] Installing backend dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt -q
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo [3/4] Creating .env file...
(
    echo # Hugging Face API Configuration
    echo HF_API_KEY=%HF_API_KEY%
    echo # Backend Configuration
    echo BACKEND_HOST=0.0.0.0
    echo BACKEND_PORT=8000
) > .env

echo [4/4] Backend setup complete!
echo.
echo Backend is ready to run. To start it:
echo   1. Open a PowerShell/CMD window
echo   2. Navigate to the backend folder
echo   3. Run: python main.py
echo.
echo Backend will be available at: http://localhost:8000
echo API Docs at: http://localhost:8000/docs
echo.
cd ..

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   Frontend Setup Instructions                         ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo To setup the frontend:
echo   1. Open a new PowerShell/CMD window
echo   2. Navigate to the frontend folder
echo   3. Run: npm install
echo   4. Run: npm start
echo.
echo Frontend will be available at: http://localhost:3000
echo.

echo ╔════════════════════════════════════════════════════════╗
echo ║   Quick Commands                                      ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo Backend:
echo   python main.py              - Start backend server
echo   http://localhost:8000/docs  - API Documentation
echo.
echo Frontend:
echo   npm start                   - Start development server
echo   npm run build               - Create production build
echo.

pause
