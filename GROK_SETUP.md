# 🤖 Teacher Assistant Bot - Grok Setup Guide

## Switched to Grok API (xAI)

Your app is now configured to use **Grok** (xAI's language model) instead of Hugging Face!

## 🔑 Getting Your Grok API Key

### Step 1: Create xAI Account
1. Go to https://console.x.ai/
2. Sign up or login with your account
3. Create an API key in the dashboard

### Step 2: Add API Key to Project
Edit `backend/.env`:

```env
# Grok API Configuration
GROK_API_KEY="xai-..."
```

Replace `xai-...` with your actual Grok API key from the xAI dashboard.

## 📝 What Changed

| Component | Before | After |
|-----------|--------|-------|
| Provider | Hugging Face | Grok (xAI) |
| API Endpoint | `api-inference.huggingface.co` | `api.x.ai/v1/chat/completions` |
| Model | zephyr-7b-beta | grok-2 |
| Config | `HF_API_KEY` | `GROK_API_KEY` |

## 📁 Updated Files

1. **backend/config.py** - Grok API configuration
2. **backend/utils.py** - Grok API calls (query_grok function)
3. **backend/.env** - Grok API key placeholder
4. **demo.ipynb** - Demo notebook using Grok

## 🚀 Running the App

### Terminal 1 - Backend
```powershell
cd "c:\Users\prana\OneDrive\Desktop\Teacher_Assistant\backend"
.\venv\Scripts\python.exe main.py
```

### Terminal 2 - Frontend
```powershell
cd "c:\Users\prana\OneDrive\Desktop\Teacher_Assistant\frontend"
npm start
```

Visit: http://localhost:3000

## ✅ Testing Grok API

Run the demo notebook (`demo.ipynb`) to test Grok directly:

1. Cell 1: Sets up Grok credentials
2. Cell 2: Shows configuration
3. Cell 3: Tests with a simple prompt

## 🔄 All Features Using Grok

- ✅ **Chat**: /api/chat/send
- ✅ **Teaching Advice**: /api/chat/teaching-advice
- ✅ **Curriculum Help**: /api/chat/curriculum-help
- ✅ **Classroom Management**: /api/chat/classroom-management
- ✅ **Assessment Help**: /api/chat/assessment-help
- ✅ **Differentiation Strategies**: /api/chat/differentiation-strategies
- ✅ **Question Generation**: /api/questions/generate
- ✅ **Answer Evaluation**: /api/evaluation/evaluate-answer
- ✅ **Lesson Planning**: /api/lesson-plan/create

## 🎯 Key Benefits of Grok

- Faster response times
- Better reasoning capabilities
- Cleaner API (OpenAI-compatible format)
- Supports latest models
- Easy to extend with new models

## 📚 Grok API Documentation

Visit: https://docs.x.ai/

## 💡 Next Steps

1. **Get Grok API Key**: https://console.x.ai/
2. **Add to .env**: Update `backend/.env` with your key
3. **Restart Backend**: Stop and run backend again
4. **Test in UI**: Open browser and try all features
5. **Check Console**: Press F12 in browser to see any errors

## 🆘 Troubleshooting

**Error: "GROK_API_KEY not set in environment"**
- Make sure you added the key to `backend/.env`
- Restart the backend server
- Verify the key starts with `xai-`

**Error: "401 Unauthorized"**
- Check your API key is correct
- Make sure it hasn't expired in xAI console
- Regenerate a new key if needed

**Empty responses**
- Check that Grok's models are available
- Try the demo notebook first
- Check backend logs for API errors

## 📞 Support

All core functionality works with Grok:
- Text generation
- Question answering
- Conversational AI
- Content evaluation

See the routes in `backend/routes/` for API details.

---

**Happy teaching with Grok! 🚀**
