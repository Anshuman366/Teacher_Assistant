#!/usr/bin/env python3
"""
Diagnostic script to check Teacher Assistant Bot setup and API connectivity
"""

import os
import sys
import json
from pathlib import Path

def check_env_file():
    """Check if .env file exists and has API key"""
    print("\n" + "="*60)
    print("🔍 CHECKING .env FILE")
    print("="*60)
    
    env_path = Path("backend/.env")
    if env_path.exists():
        print("✓ .env file found")
        with open(env_path, 'r') as f:
            content = f.read()
            if "HF_API_KEY" in content:
                print("✓ HF_API_KEY present in .env")
                # Check if it's not just placeholder
                if "hf_" in content:
                    print("✓ API key appears to be set (starts with 'hf_')")
                else:
                    print("❌ API key might be placeholder or invalid")
            else:
                print("❌ HF_API_KEY not found in .env")
    else:
        print("❌ .env file not found in backend/")
        print("   Create it with: HF_API_KEY=your_token_here")

def check_config():
    """Check if config.py can be imported"""
    print("\n" + "="*60)
    print("🔍 CHECKING CONFIG.PY")
    print("="*60)
    
    try:
        sys.path.insert(0, 'backend')
        import config
        print("✓ config.py imports successfully")
        print(f"  - Models configured: {list(config.MODELS.keys())}")
        print(f"  - Upload directory: {config.UPLOAD_DIR}")
        print(f"  - API Key loaded: {'YES' if config.HF_API_KEY else 'NO'}")
        return True
    except Exception as e:
        print(f"❌ Error importing config.py: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\n" + "="*60)
    print("🔍 CHECKING DEPENDENCIES")
    print("="*60)
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'requests',
        'python-dotenv',
        'PyPDF2',
        'PIL',
        'pydantic'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package if package != 'PIL' else 'PIL')
            print(f"✓ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Install missing packages with:")
        print(f"   pip install {' '.join(missing)}")
        return False
    return True

def test_hf_api():
    """Test Hugging Face API connectivity"""
    print("\n" + "="*60)
    print("🔍 TESTING HUGGING FACE API")
    print("="*60)
    
    try:
        sys.path.insert(0, 'backend')
        import config
        import requests
        
        if not config.HF_API_KEY:
            print("❌ HF_API_KEY not set")
            return False
        
        # Test with a simple query
        model_name = "HuggingFaceH4/zephyr-7b-beta"
        url = f"https://api-inference.huggingface.co/models/{model_name}"
        headers = {"Authorization": f"Bearer {config.HF_API_KEY}"}
        payload = {"inputs": "Hello, this is a test"}
        
        print(f"Testing model: {model_name}")
        print("Sending test request to Hugging Face API...")
        
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✓ API is responding correctly")
            print(f"  Response: {response.json()}")
            return True
        elif response.status_code == 503:
            print("⚠️  Model is loading (try again in a moment)")
            return False
        else:
            print(f"❌ API error: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def check_backend_routes():
    """Check if backend routes are properly configured"""
    print("\n" + "="*60)
    print("🔍 CHECKING BACKEND ROUTES")
    print("="*60)
    
    try:
        sys.path.insert(0, 'backend')
        from routes import document, questions, evaluation, lesson_plan, chat
        
        routes_to_check = {
            'document': document.router,
            'questions': questions.router,
            'evaluation': evaluation.router,
            'lesson_plan': lesson_plan.router,
            'chat': chat.router
        }
        
        for name, router in routes_to_check.items():
            if router and router.routes:
                print(f"✓ {name} router loaded - {len(router.routes)} endpoints")
            else:
                print(f"❌ {name} router problem")
        
        return True
    except Exception as e:
        print(f"❌ Error checking routes: {e}")
        return False

def check_frontend_files():
    """Check if frontend files exist"""
    print("\n" + "="*60)
    print("🔍 CHECKING FRONTEND FILES")
    print("="*60)
    
    frontend_files = [
        'frontend/package.json',
        'frontend/src/App.js',
        'frontend/src/api/index.js',
        'frontend/src/pages/ChatBot.js',
        'frontend/src/pages/QuestionGenerator.js',
    ]
    
    for file in frontend_files:
        if Path(file).exists():
            print(f"✓ {file}")
        else:
            print(f"❌ {file} - MISSING")

def check_uploads_dir():
    """Check if uploads directory exists"""
    print("\n" + "="*60)
    print("🔍 CHECKING UPLOADS DIRECTORY")
    print("="*60)
    
    uploads_path = Path("backend/uploads")
    if uploads_path.exists():
        print(f"✓ uploads/ directory exists")
    else:
        print(f"⚠️  uploads/ directory doesn't exist - creating...")
        uploads_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ uploads/ directory created")

def print_summary(results):
    """Print diagnostic summary"""
    print("\n" + "="*60)
    print("📋 DIAGNOSTIC SUMMARY")
    print("="*60)
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n✅ ALL CHECKS PASSED!")
        print("\nYour setup is ready. Run:")
        print("  Backend:  cd backend && python main.py")
        print("  Frontend: cd frontend && npm start")
    else:
        print("\n⚠️  SOME ISSUES FOUND:")
        for check, passed in results.items():
            status = "✓" if passed else "❌"
            print(f"  {status} {check}")
        
        print("\n📝 NEXT STEPS:")
        print("  1. Fix the failed checks above")
        print("  2. Ensure HF_API_KEY is set in backend/.env")
        print("  3. Install missing dependencies: pip install -r backend/requirements.txt")
        print("  4. Then try running the servers again")

def main():
    print("\n" + "🚀 "*30)
    print("TEACHER ASSISTANT BOT - DIAGNOSTIC TOOL")
    print("🚀 "*30)
    
    results = {
        "Dependencies": check_dependencies(),
        "Config File": check_config(),
        "Backend Routes": check_backend_routes(),
        "Frontend Files": True,  # Just info
        "Uploads Directory": True,  # Auto-created
        "Hugging Face API": test_hf_api(),
    }
    
    check_frontend_files()
    check_uploads_dir()
    print_summary(results)
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
