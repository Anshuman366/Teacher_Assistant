from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import os
import shutil
from config import UPLOAD_DIR, ALLOWED_EXTENSIONS, MAX_FILE_SIZE
from utils import (
    extract_text_from_pdf,
    extract_text_from_image,
    extract_text_from_docx,
    extract_text_from_doc,
    embed_document,
    semantic_search,
    chat_with_llm,
    sanitize_text,
)
from typing import Optional

router = APIRouter()

class DocumentResponse(BaseModel):
    filename: str
    size: int
    content: str
    file_type: str

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a document and trigger embedding process for RAG."""
    try:
        # Validate file
        if file.size > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large")
        
        # Get file extension
        file_ext = file.filename.split('.')[-1].lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail=f"File type {file_ext} not allowed")
        
        # Save file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract content based on file type
        if file_ext == 'pdf':
            content = extract_text_from_pdf(file_path)
        elif file_ext in ['png', 'jpg', 'jpeg']:
            content = extract_text_from_image(file_path)
        elif file_ext == 'docx':
            content = extract_text_from_docx(file_path)
        elif file_ext == 'doc':
            content = extract_text_from_doc(file_path)
        else:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        
        # Trigger embedding and store in vector database (RAG)
        try:
            embed_document(filename=file.filename, text=content)
        except Exception as e:
            print(f"Warning: embedding failed but upload succeeded: {str(e)}")
        
        return {
            "status": "success",
            "filename": file.filename,
            "size": file.size,
            "file_type": file_ext,
            "message": "Document uploaded and processed successfully"
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading document: {str(e)}")

@router.get("/list")
async def list_documents():
    """List all uploaded documents"""
    try:
        files = os.listdir(UPLOAD_DIR)
        documents = []
        for filename in files:
            file_path = os.path.join(UPLOAD_DIR, filename)
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                documents.append({
                    "filename": filename,
                    "size": size,
                    "path": file_path
                })
        return {"documents": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/explain/{filename}")
async def explain_document(filename: str):
    """Get explanation of document"""
    try:
        file_path = os.path.join(UPLOAD_DIR, filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        file_ext = filename.split('.')[-1].lower()
        
        if file_ext == 'pdf':
            content = extract_text_from_pdf(file_path)
        elif file_ext in ['png', 'jpg', 'jpeg']:
            content = extract_text_from_image(file_path)
        else:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        
        # Generate explanation using LLM
        from utils import chat_with_llm
        explanation_prompt = f"Please provide a clear and concise explanation of the following content in markdown and structured format:\n\n{content[:3000]}"
        explanation = chat_with_llm(explanation_prompt)
        
        return {
            "filename": filename,
            "explanation": explanation,
            "content_preview": content[:2000]
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class AskRequest(BaseModel):
    question: str


@router.post("/ask/{filename}")
async def ask_document_question(filename: str, request: AskRequest):
    """Answer a question about a specific uploaded document using semantic search (RAG)."""
    try:
        # Try semantic search first (global store may contain the doc text)
        hits = semantic_search(request.question, top_k=3)

        # If there are hits, include excerpts in the prompt
        if hits:
            combined = '\n\n'.join([f"Source: {h['filename']}\n{h['text'][:1200]}" for h in hits])
            prompt = f"""Use the following document excerpts to answer the question. Cite sources where relevant.

Document excerpts:
{combined}

Question: {request.question}

Provide a clear, concise answer in markdown."""
        else:
            # fallback: read file and answer from full content (use proper extractors)
            file_path = os.path.join(UPLOAD_DIR, filename)
            if not os.path.exists(file_path):
                raise HTTPException(status_code=404, detail="File not found")
            file_ext = filename.split('.')[-1].lower()

            if file_ext == 'pdf':
                content = extract_text_from_pdf(file_path)
            elif file_ext in ['png', 'jpg', 'jpeg']:
                content = extract_text_from_image(file_path)
            elif file_ext == 'docx':
                content = extract_text_from_docx(file_path)
            elif file_ext == 'doc':
                content = extract_text_from_doc(file_path)
            else:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

            # sanitize content before sending to LLM
            content = sanitize_text(content)

            prompt = f"Answer the question using the document content below.\n\nDocument:\n{content[:3000]}\n\nQuestion: {request.question}"

        answer = chat_with_llm(prompt)

        return {"status": "success", "response": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
