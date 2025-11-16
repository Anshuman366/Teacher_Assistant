# Installation Guide

## Option 1: Local Installation (Recommended for Development)

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git
- Hugging Face API Key

### Step-by-Step Installation

#### 1. Clone or Download Project
```bash
git clone <repository-url>
cd Teacher_Assistant
```

#### 2. Setup Backend
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env
# Edit .env and add your Hugging Face API key

# Run server
python main.py
```

#### 3. Setup Frontend (in new terminal)
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

#### 4. Access Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Option 2: Docker Installation (Production-ready)

### Prerequisites
- Docker
- Docker Compose
- Hugging Face API Key

### Installation Steps

#### 1. Navigate to Project
```bash
cd Teacher_Assistant
```

#### 2. Create .env File
```bash
echo HF_API_KEY=your_api_key_here > .env
```

#### 3. Build and Run with Docker Compose
```bash
# Development
docker-compose up

# Production
docker-compose -f docker-compose.prod.yml up
```

#### 4. Access Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

---

## Option 3: Cloud Deployment

### Deploy Backend to Heroku
```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set HF_API_KEY=your_api_key

# Deploy
git push heroku main
```

### Deploy Frontend to Vercel
1. Push code to GitHub
2. Connect GitHub repo to Vercel
3. Set environment variable: REACT_APP_API_URL=https://your-heroku-app.herokuapp.com/api
4. Deploy automatically on push

### Deploy to AWS
1. Use EC2 for backend
2. Use S3 + CloudFront for frontend
3. Or use AWS Amplify for full stack deployment

### Deploy to Azure
1. Use Azure App Service for backend
2. Use Azure Static Web Apps for frontend
3. Use Azure Key Vault for secrets

---

## Verification

### Test Backend
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy"}
```

### Test Frontend
Open browser and navigate to http://localhost:3000

### Test API
Visit http://localhost:8000/docs for interactive API documentation

---

## Troubleshooting

### Python Issues
- Ensure Python 3.8+ installed: `python --version`
- Use virtual environment to avoid conflicts
- Reinstall packages: `pip install -r requirements.txt --force-reinstall`

### Node/NPM Issues
- Ensure Node 16+ installed: `node --version`
- Clear npm cache: `npm cache clean --force`
- Reinstall packages: `rm -rf node_modules && npm install`

### API Key Issues
- Verify key is valid at https://huggingface.co/settings/tokens
- Ensure .env file has correct format
- Restart backend after updating .env

### Port Conflicts
```bash
# Windows - Find process on port 8000
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F

# Or change port in main.py
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Connection Refused
- Check if services are running
- Verify firewall settings
- Use correct localhost URLs

---

## Performance Optimization

### Backend
- Use async operations for I/O
- Implement caching for frequently used data
- Use connection pooling for databases

### Frontend
- Enable gzip compression
- Optimize images
- Use lazy loading
- Implement service workers

### General
- Use CDN for static assets
- Implement rate limiting
- Use database indexing

---

## Security Considerations

1. **API Key Management**
   - Never commit .env files
   - Use environment variables
   - Rotate keys regularly

2. **File Upload**
   - Validate file types
   - Scan for malware
   - Limit file sizes
   - Store in secure location

3. **CORS**
   - Configure allowed origins
   - Use secure headers
   - Implement CSRF protection

4. **Data Privacy**
   - Don't store sensitive data
   - Use HTTPS
   - Implement access controls

---

## Maintenance

### Regular Updates
```bash
# Update Python packages
pip install --upgrade -r requirements.txt

# Update npm packages
npm update
```

### Monitoring
- Monitor API response times
- Check error logs
- Track usage statistics
- Monitor server resources

### Backups
- Backup uploaded documents
- Backup user data
- Backup configuration files
- Store backups securely

---

## Support & Help

- **Documentation**: See README.md
- **Quick Start**: See QUICKSTART.md
- **Issues**: Create GitHub issue
- **API Docs**: Visit http://localhost:8000/docs

---

**Installation Complete! Happy Teaching! 🎓**
