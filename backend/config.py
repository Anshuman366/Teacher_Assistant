import os
from dotenv import load_dotenv

load_dotenv()

# Grok API Configuration (xAI)
GROK_API_KEY = os.getenv("GROK_API_KEY", "")
GROK_API_URL = "https://api.x.ai/v1/chat/completions"
GROK_MODEL = "llama-3.1-8b-instant"

# Configuration
API_PROVIDER = "grok"  # Using Grok instead of Hugging Face


# Upload settings
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {"pdf", "txt", "doc", "docx", "png", "jpg", "jpeg"}

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
