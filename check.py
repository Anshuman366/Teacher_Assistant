import sys
import os

print("=" * 60)
print("TEACHER ASSISTANT BOT - QUICK DIAGNOSTIC")
print("=" * 60)

# Check working directory
print(f"\n📁 Current directory: {os.getcwd()}")

# Check if .env exists
if os.path.exists("backend/.env"):
    print("✓ backend/.env found")
    with open("backend/.env") as f:
        content = f.read()
        if "HF_API_KEY" in content and "hf_" in content:
            print("✓ HF_API_KEY is set")
        else:
            print("❌ HF_API_KEY may not be properly set")
else:
    print("❌ backend/.env NOT found")

# Check dependencies
print("\n📦 Checking Python packages...")
packages = ['fastapi', 'uvicorn', 'requests', 'dotenv', 'PyPDF2']
for pkg in packages:
    try:
        __import__(pkg.replace('dotenv', 'dotenv'))
        print(f"  ✓ {pkg}")
    except:
        print(f"  ❌ {pkg} MISSING")

# Check if we can import config
print("\n⚙️  Checking backend config...")
sys.path.insert(0, 'backend')
try:
    import config
    print(f"  ✓ config.py loads")
    print(f"  ✓ API Key set: {bool(config.HF_API_KEY)}")
    print(f"  ✓ Models: {list(config.MODELS.keys())}")
except Exception as e:
    print(f"  ❌ Error: {e}")

# Check frontend
print("\n📱 Checking frontend...")
if os.path.exists("frontend/package.json"):
    print("  ✓ frontend/package.json exists")
else:
    print("  ❌ frontend/package.json NOT found")

print("\n" + "=" * 60)
print("✅ Diagnostic complete")
print("=" * 60)
