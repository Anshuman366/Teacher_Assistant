# Quick Start Guide 🚀

Get the Teacher Assistant Bot up and running in minutes!

## Step 1: Get Hugging Face API Key

1. Visit https://huggingface.co
2. Sign up (free account)
3. Go to Settings > Access Tokens
4. Create new token (read access)
5. Copy the token

## Step 2: Setup Backend

### Windows PowerShell:
```powershell
cd backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment file
copy .env.example .env

# Edit .env and add your Hugging Face API key
notepad .env
# Add: HF_API_KEY=your_token_here

# Run server
python main.py
```

Backend will start on `http://localhost:8000`

## Step 3: Setup Frontend

### New PowerShell Window:
```powershell
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will open on `http://localhost:3000`

## Step 4: Start Using!

1. **Document Analysis**: Upload a PDF or document to analyze
2. **Generate Questions**: Create practice questions from your content
3. **Evaluate Answers**: Get AI feedback on student answers
4. **Lesson Planner**: Create structured lesson plans
5. **Chat Bot**: Ask teaching questions and get advice

## API Status Check

Once backend is running, check API:
- Status: http://localhost:8000/health
- Documentation: http://localhost:8000/docs

## First Time Tips

1. **Small Files First**: Test with small documents initially
2. **Rate Limiting**: Free Hugging Face tier has rate limits - wait if needed
3. **Clear Prompts**: Give clear input for better AI responses
4. **Save Work**: Copy/export your results as they aren't auto-saved

## Common Commands

```bash
# Backend
cd backend
.\venv\Scripts\activate          # Activate virtual env
pip install -r requirements.txt  # Install packages
python main.py                   # Run server

# Frontend
cd frontend
npm install                      # Install packages
npm start                        # Run dev server
npm run build                    # Create production build
```

## Troubleshooting

### Port Already in Use?
Backend (port 8000):
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

Frontend (port 3000):
```powershell
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Module Not Found?
```powershell
pip install -r requirements.txt  # Backend
npm install                      # Frontend
```

### API Connection Error?
- Ensure backend is running
- Check `.env` has correct API key
- Verify URLs in frontend config

## Next Steps

1. Explore all 5 main features
2. Read main `README.md` for detailed documentation
3. Check individual backend/frontend README files
4. Customize colors and settings
5. Consider deploying to cloud

## Need Help?

1. Check README.md files
2. Review error messages carefully
3. Verify environment variables
4. Check network connectivity
5. Ensure all dependencies installed

---

**You're all set! Happy teaching! 🎓**
