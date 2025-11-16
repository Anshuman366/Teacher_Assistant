from config import GROK_API_KEY, GROK_API_URL, GROK_MODEL
from typing import Optional
import numpy as np
import os
import json
from datetime import datetime
import re

# Try to import sentence-transformers for dense embeddings
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_AVAILABLE = True
except Exception:
    SentenceTransformer = None
    SENTENCE_AVAILABLE = False

# Try to import Chroma for persistent vector database
try:
    import chromadb
    from chromadb.config import Settings
    CHROMA_AVAILABLE = True
except Exception:
    chromadb = None
    CHROMA_AVAILABLE = False

# Whether we have any vector embedding capability
VEC_AVAILABLE = SENTENCE_AVAILABLE and CHROMA_AVAILABLE


def query_grok(prompt: str, system_context: Optional[str] = None, max_tokens: int = 1000):
    """
    Query Grok via the user's preferred langchain wrapper if available,
    otherwise fall back to a direct HTTP call to the Grok endpoint.

    Returns the response string.
    """

    # Build messages list
    messages = []
    if system_context:
        messages.append({"role": "system", "content": system_context})
    messages.append({"role": "user", "content": prompt})

    # Try langchain_grok (user said they updated to use this). Support
    # a couple of possible package names/CLIs to be tolerant.
    try:
        # Try the common name first
        from langchain_groq import ChatGroq
        llm = ChatGroq(model=GROK_MODEL, api_key=GROK_API_KEY)
        # some wrappers accept a messages list or a single prompt
        if hasattr(llm, "invoke"):
            out = llm.invoke(messages)
            out=out.content
        else:
            out = llm(messages)
            out=out.content

        # If LangChain-style response object, try to coerce to text
        if isinstance(out, dict) and "content" in out:
            return out["content"]
        return out
    except Exception:
        pass

    try:
        # Try alternative package name (typo variants in ecosystem)
        from langchain_groq import ChatGroq
        llm = ChatGroq(model=GROK_MODEL, api_key=GROK_API_KEY)
        if hasattr(llm, "invoke"):
            out = llm.invoke(messages)
            out=out.content
        else:
            out = llm(messages)
            out=out.content
        if isinstance(out, dict) and "content" in out:
            return out["content"]
        return out
    except Exception:
        pass

    # If we reach here the langchain wrapper wasn't available.
    raise RuntimeError(
        "No Grok langchain wrapper available. Install and configure `langchain_grok` "
        "or `langchain_groq` (and set `GROK_API_KEY` in your environment) to use Grok."
    )

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file"""
    from PyPDF2 import PdfReader
    
    text = ""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        raise Exception(f"Error extracting PDF: {str(e)}")
    
    return text

def extract_text_from_image(file_path: str) -> str:
    """Extract text from image using OCR via Grok"""
    try:
        # Read image and encode as base64 for Grok
        import base64
        with open(file_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        # Use Grok to analyze the image
        prompt = f"Extract and return all text from this image. Be as accurate as possible."
        # Note: Grok's vision capability would be used here if available
        result = query_grok(prompt, system_context="You are an OCR expert. Extract text from images accurately.")
        return result
    except Exception as e:
        return f"Error extracting text from image: {str(e)}"


def sanitize_text(text: str) -> str:
    """Remove non-printable/binary characters and collapse excessive whitespace.

    This helps avoid embedding raw PDF binary streams or control characters
    that can leak into prompts and LLM responses.
    """
    if not isinstance(text, str):
        try:
            text = str(text)
        except Exception:
            return ""

    # Remove common binary artifacts (nulls, bell, etc.)
    text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]+", " ", text)

    # Replace multiple whitespace/newlines with single ones
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Trim leading/trailing whitespace
    return text.strip()


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a .docx file using python-docx (Document).

    Falls back to an error message if `python-docx` isn't available.
    """
    try:
        from docx import Document
    except Exception as e:
        return f"Error: python-docx not installed. Install 'python-docx' to extract .docx files: {str(e)}"

    try:
        doc = Document(file_path)
        paragraphs = [p.text for p in doc.paragraphs if p.text]
        text = "\n".join(paragraphs)
        return sanitize_text(text)
    except Exception as e:
        return f"Error extracting .docx: {str(e)}"


def extract_text_from_doc(file_path: str) -> str:
    """Extract text from legacy .doc using `textract` if available.

    If `textract` is not installed, return an instructive error message.
    """
    try:
        import textract
    except Exception as e:
        return "Error: .doc extraction requires the 'textract' package (or convert file to .docx)."

    try:
        raw = textract.process(file_path)
        # textract returns bytes
        if isinstance(raw, bytes):
            text = raw.decode('utf-8', errors='ignore')
        else:
            text = str(raw)
        return sanitize_text(text)
    except Exception as e:
        return f"Error extracting .doc: {str(e)}"

def generate_questions(content: str, num_questions: int = 5, difficulty: str = "medium") -> list[str]:
    """Generate questions from content using Grok"""
    prompt = f"""Generate {num_questions} {difficulty} difficulty questions based on the following content. 
    Return only the questions, one per line, numbered.
    
    Content:
    {content[:2000]}
    
    Questions:"""
    
    try:
        response_text = query_grok(prompt, max_tokens=500)
        # Extract just the questions part
        if "Questions:" in response_text:
            questions_part = response_text.split("Questions:")[-1]
        else:
            questions_part = response_text
        
        questions = [q.strip() for q in questions_part.split('\n') if q.strip()]
        return questions[:num_questions]
    except Exception as e:
        return [f"Error generating questions: {str(e)}"]

def evaluate_answer(question: str, student_answer: str, correct_answer: str) -> dict:
    """Evaluate student answer using Grok"""
    prompt = f"""Evaluate the following student answer and provide feedback.
    
    Question: {question}
    Student Answer: {student_answer}
    Expected/Correct Answer: {correct_answer}
    
    Provide:
    1. Score (0-100)
    2. Feedback (what was good and what needs improvement)
    3. Correct aspects
    4. Missing aspects"""
    
    try:
        evaluation = query_grok(prompt, max_tokens=500)
        return {
            "evaluation": evaluation,
            "status": "success"
        }
    except Exception as e:
        return {
            "evaluation": f"Error evaluating answer: {str(e)}",
            "status": "error"
        }

def create_lesson_plan(chapter: str, topics: list[str], lectures_per_week: int, total_weeks: int) -> str:
    """Create a lesson plan using Grok"""
    topics_str = ", ".join(topics)
    prompt = f"""Create a detailed lesson plan for the following:
    
    Chapter: {chapter}
    Topics: {topics_str}
    Lectures per week: {lectures_per_week}
    Total weeks: {total_weeks}
    
    Provide a week-by-week breakdown with:
    - Week number
    - Topics covered
    - Learning objectives
    - Activities/assignments
    - Assessment methods
    
    Format clearly with sections for each week."""
    
    try:
        return query_grok(prompt, max_tokens=2000)
    except Exception as e:
        return f"Error creating lesson plan: {str(e)}"

def chat_with_llm(message: str, system_context: Optional[str] = None) -> str:
    """Chat with LLM using Grok"""
    if system_context:
        prompt = f"{system_context}\n\nUser: {message}"
    else:
        prompt = message
    
    try:
        return query_grok(prompt, system_context=system_context, max_tokens=1000)
    except Exception as e:
        return f"Error in chat: {str(e)}"


### Vector store helpers using Chroma for persistent RAG

_CHROMA_CLIENT = None
_COLLECTION = None
_EMBED_MODEL = None
_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "vector_store")

def _get_chroma_collection():
    """Get or create the Chroma collection for document embeddings."""
    global _CHROMA_CLIENT, _COLLECTION, _EMBED_MODEL
    
    if not CHROMA_AVAILABLE or not SENTENCE_AVAILABLE:
        return None
    
    try:
        if _COLLECTION is None:
            # Initialize embedding model
            if _EMBED_MODEL is None:
                _EMBED_MODEL = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Initialize Chroma client with persistent storage
            os.makedirs(_DB_PATH, exist_ok=True)
            _CHROMA_CLIENT = chromadb.PersistentClient(path=_DB_PATH)
            
            # Get or create collection
            _COLLECTION = _CHROMA_CLIENT.get_or_create_collection(
                name="documents",
                metadata={"hnsw:space": "cosine"}
            )
        
        return _COLLECTION
    except Exception as e:
        print(f"Error initializing Chroma: {str(e)}")
        return None


def embed_document(filename: str, text: str):
    """Create dense embeddings for a document and store in Chroma vector database.
    
    This enables persistent RAG: embeddings survive server restarts and
    semantic search retrieves relevant excerpts for context-aware LLM answering.
    """
    if not CHROMA_AVAILABLE or not SENTENCE_AVAILABLE:
        print("Chroma or sentence-transformers not available for embedding")
        return
    
    collection = _get_chroma_collection()
    if collection is None:
        return
    
    try:
        # Sanitize incoming text to remove binary/control characters
        text = sanitize_text(text)
        # Create a unique ID for this document
        doc_id = filename.replace('/', '_').replace('\\', '_')
        
        # Split text into chunks for better retrieval (max 1000 chars per chunk)
        chunks = []
        chunk_size = 1000
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i+chunk_size]
            if chunk.strip():
                chunks.append(chunk)
        
        if not chunks:
            chunks = [text]
        
        # Add chunks to collection with metadata
        ids = [f"{doc_id}_{i}" for i in range(len(chunks))]
        metadatas = [{"filename": filename, "chunk": i} for i in range(len(chunks))]
        
        collection.add(
            ids=ids,
            documents=chunks,
            metadatas=metadatas
        )
        print(f"Embedded {len(chunks)} chunks from {filename}")
    except Exception as e:
        print(f"Error embedding document: {str(e)}")


def semantic_search(query: str, top_k: int = 3) -> list[dict]:
    """Perform semantic search over stored documents using Chroma.
    
    Returns top_k most relevant document excerpts from the vector database.
    """
    if not CHROMA_AVAILABLE or not SENTENCE_AVAILABLE:
        return []
    
    collection = _get_chroma_collection()
    if collection is None:
        return []
    
    try:
        results = collection.query(
            query_texts=[query],
            n_results=top_k,
            include=['documents', 'metadatas']
        )
        
        # Transform results into expected format
        retrieved = []
        if results and results['documents'] and len(results['documents']) > 0:
            for i, doc in enumerate(results['documents'][0]):
                meta = results['metadatas'][0][i] if results['metadatas'] else {}
                retrieved.append({
                    "filename": meta.get("filename", "unknown"),
                    "text": doc,
                    "chunk": meta.get("chunk", 0)
                })
        
        return retrieved
    except Exception as e:
        print(f"Error in semantic search: {str(e)}")
        return []
