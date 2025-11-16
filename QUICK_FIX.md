# 🚀 QUICK START - Get Your Bot Running in 3 Minutes

## The Problem You Had
❌ Clicked buttons but saw no text on UI  
✅ **FIXED** - Updated backend API responses to match frontend

## Setup (One Time Only)

### Terminal 1 - Backend Setup
```powershell
cd "c:\Users\prana\OneDrive\Desktop\Teacher_Assistant"
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Terminal 2 - Frontend Setup  
```powershell
cd "c:\Users\prana\OneDrive\Desktop\Teacher_Assistant"
cd frontend
npm install
```

---

## Running the App (Every Time)

### Terminal 1 - Start Backend
```powershell
cd "c:\Users\prana\OneDrive\Desktop\Teacher_Assistant\backend"
.\venv\Scripts\activate
python main.py
```

**Wait for:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Terminal 2 - Start Frontend
```powershell
cd "c:\Users\prana\OneDrive\Desktop\Teacher_Assistant\frontend"
npm start
```

**Wait for browser to open at:**
```
http://localhost:3000
```

---

## Test It!

✅ **Chat Bot**
- Click "Chat Bot" tab
- Type: "How do I teach fractions?"
- Click Send
- **You should see AI response appear** ✨

✅ **Question Generator**
- Click "Question Generator" tab
- Paste some content
- Click "Generate Questions"
- **Questions should appear** ✨

✅ **Other Features**
- Try Document Analyzer
- Try Answer Evaluator  
- Try Lesson Planner

---

## 🆘 If Backend Won't Start

**Error: "ModuleNotFoundError: No module named 'fastapi'"**

Fix:
```powershell
# Make sure you're in backend directory
cd backend
# Make sure venv is activated (should see (venv) in prompt)
.\venv\Scripts\activate
# Install again
pip install -r requirements.txt -v
```

**Error: "No module named 'dotenv'"**

Same fix as above.

**Error: "HF_API_KEY not set"**

```powershell
# Check your API key
cat backend\.env
# Should contain: HF_API_KEY=hf_xxxxx...

# If blank or missing, edit backend/.env:
notepad backend\.env
```

Add your key:
```
HF_API_KEY=hf_your_token_here
```

---

## 🆘 If Frontend Won't Start

**Error: "npm: command not found"**

Install Node.js from https://nodejs.org (v16+)

**Error: Module not found**

```powershell
cd frontend
npm install
npm start
```

**Port 3000 already in use**

```powershell
# Kill the process using port 3000
# Then try npm start again
taskkill /F /IM node.exe
npm start
```

---

## 🆘 If You See No Text on UI

**1. Check Backend is Running**
```powershell
# In a new terminal, run:
curl http://localhost:8000/health
# Should see: {"status":"healthy"}
```

**2. Check Browser Console for Errors**
- Press F12
- Click "Console" tab  
- Look for red error messages
- Take a screenshot and check what's wrong

**3. Check Network Tab**
- Press F12
- Click "Network" tab
- Try clicking a button
- Look for failed API requests (red)
- Click the failed request to see error

**4. Verify Files Were Updated**
```powershell
# Check chat.py has been updated
findstr /C:"class TeachingAdviceRequest" backend\routes\chat.py
# Should find the class
```

---

## 📊 The Fix Explained

### What Was Wrong
```python
# ❌ OLD - Backend expected URL params
@router.post("/teaching-advice")
async def get_teaching_advice(
    topic: str,        # URL param like ?topic=...
    challenge: str,    # URL param like ?challenge=...
):
    return {"advice": text}  # Frontend looked for "response"
```

```javascript
// ❌ OLD - Frontend sent JSON body
const response = await getTeachingAdvice({
  topic: "...",       // Frontend sent as JSON
  challenge: "..."
});
// ❌ Tried to find: response.data.response (didn't exist!)
```

### What Was Fixed
```python
# ✅ NEW - Backend accepts JSON body
class TeachingAdviceRequest(BaseModel):
    topic: str
    challenge: str

@router.post("/teaching-advice")
async def get_teaching_advice(request: TeachingAdviceRequest):
    return {
        "status": "success",
        "response": text  # ✅ Frontend now finds this!
    }
```

```javascript
// ✅ NEW - Frontend gets correct response
const response = await getTeachingAdvice({
  topic: "...",       // Sent as JSON body
  challenge: "..."
});
// ✅ Works: response.data.response ✅
```

---

## ✨ All Features Working Now

| Feature | Status |
|---------|--------|
| 💬 ChatBot | ✅ Fixed |
| 🧠 Question Generator | ✅ Fixed |
| ✅ Answer Evaluator | ✅ Fixed |
| 📅 Lesson Planner | ✅ Fixed |
| 📄 Document Analyzer | ✅ Works |

---

## 🎯 One-Liner Shortcuts

**Start Everything (Terminal 1):**
```powershell
cd "c:\Users\prana\OneDrive\Desktop\Teacher_Assistant\backend"; .\venv\Scripts\activate; python main.py
```

**Start Everything (Terminal 2):**
```powershell
cd "c:\Users\prana\OneDrive\Desktop\Teacher_Assistant\frontend"; npm start
```

**Check Status:**
```powershell
cd "c:\Users\prana\OneDrive\Desktop\Teacher_Assistant"; python check.py
```

---

## 🎉 Done!

Your app should now:
- ✅ Accept input
- ✅ Call AI
- ✅ Show responses
- ✅ Work smoothly

**Start teaching with AI!** 🚀

Questions? Check TROUBLESHOOTING.md for more details.
