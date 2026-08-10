import os
import json
import uuid
import time
import requests
from typing import List, Dict, Any, Optional, Tuple
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import (
    init_db, create_session, get_sessions, delete_session,
    add_message, get_session_messages, add_document, get_documents, delete_document
)
from system_monitor import get_system_metrics
from rag_engine import rag_engine, UPLOAD_DIR
from voice_assistant import execute_voice_command

OLLAMA_URL = "http://localhost:11434"
DEFAULT_MODEL = "qwen3:1.7b"

app = FastAPI(title="Device Manager API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
init_db()

# Mount static directory
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class ChatRequest(BaseModel):
    session_id: str
    message: str
    model: Optional[str] = DEFAULT_MODEL
    temperature: Optional[float] = 0.7
    use_rag: Optional[bool] = True

class VoiceCommandRequest(BaseModel):
    command: str

@app.get("/", response_class=HTMLResponse)
def read_root():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h2>Device Manager API Running. Static UI loading...</h2>")

@app.get("/api/system")
def api_system_metrics():
    metrics = get_system_metrics()
    ollama_online = False
    active_model = DEFAULT_MODEL
    available_models = []
    
    try:
        res = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        if res.status_code == 200:
            ollama_online = True
            models_data = res.json().get("models", [])
            available_models = [m.get("name") for m in models_data]
            if available_models:
                active_model = available_models[0]
    except Exception:
        ollama_online = False
        
    metrics["ollama"] = {
        "online": ollama_online,
        "active_model": active_model,
        "available_models": available_models
    }
    return metrics

@app.get("/api/models")
def api_get_models():
    try:
        res = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        pass
    return {"models": [{"name": DEFAULT_MODEL, "details": {"parameter_size": "1.7B"}}]}

@app.get("/api/sessions")
def api_get_sessions():
    return get_sessions()

@app.post("/api/sessions")
def api_create_session(title: str = "New Conversation"):
    session_id = str(uuid.uuid4())
    return create_session(session_id, title)

@app.delete("/api/sessions/{session_id}")
def api_delete_session(session_id: str):
    delete_session(session_id)
    return {"status": "success", "message": f"Session {session_id} deleted"}

@app.get("/api/sessions/{session_id}/messages")
def api_get_messages(session_id: str):
    return get_session_messages(session_id)

def build_prompt_with_rag(query: str, history: List[Dict[str, Any]], use_rag: bool) -> Tuple[str, List[Dict[str, Any]]]:
    sources = []
    rag_context = ""
    
    if use_rag:
        search_results = rag_engine.search(query, top_k=3)
        if search_results:
            sources = search_results
            rag_context = "\n\n[RELEVANT LOCAL KNOWLEDGE BASE CONTEXT]:\n"
            for idx, item in enumerate(search_results, 1):
                rag_context += f"--- Source {idx} ({item['filename']}) ---\n{item['snippet']}\n"
            rag_context += "--- END CONTEXT ---\nPlease incorporate relevant details from the above context if helpful.\n"

    system_prompt = (
        "You are Device Manager, a privacy-first, on-device AI assistant powered by the Qwen3 Small Language Model (SLM). "
        "You run entirely locally on the user's hardware. You provide clear, concise, accurate, and helpful answers. "
        f"{rag_context}"
    )

    full_prompt = f"System: {system_prompt}\n"
    for msg in history[-6:]: # Last 6 messages context window
        role_label = "User" if msg["role"] == "user" else "Assistant"
        full_prompt += f"{role_label}: {msg['content']}\n"
    
    full_prompt += f"User: {query}\nAssistant:"
    return full_prompt, sources

@app.post("/api/chat")
def api_chat(req: ChatRequest):
    # Save user message
    history = get_session_messages(req.session_id)
    add_message(req.session_id, "user", req.message)

    prompt, sources = build_prompt_with_rag(req.message, history, req.use_rag)

    start_time = time.time()
    model_name = req.model or DEFAULT_MODEL

    try:
        ollama_res = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": req.temperature
                }
            },
            timeout=120
        )
        if ollama_res.status_code == 200:
            data = ollama_res.json()
            reply = data.get("response", "").strip()
            total_duration_ns = data.get("total_duration", 0)
            eval_count = data.get("eval_count", 0)
            tps = round((eval_count / (total_duration_ns / 1e9)), 1) if total_duration_ns > 0 else 0.0

            msg_id = add_message(req.session_id, "assistant", reply, sources=sources, tokens_per_sec=tps)
            return {
                "id": msg_id,
                "role": "assistant",
                "content": reply,
                "sources": sources,
                "tokens_per_sec": tps,
                "model": model_name
            }
    except Exception as e:
        fallback_reply = f"[Device Manager Local Error]: Could not query Ollama engine ({str(e)}). Ensure Ollama is active locally."
        add_message(req.session_id, "assistant", fallback_reply)
        return {"role": "assistant", "content": fallback_reply, "sources": []}

@app.post("/api/chat/stream")
def api_chat_stream(req: ChatRequest):
    # Save user message
    history = get_session_messages(req.session_id)
    add_message(req.session_id, "user", req.message)

    prompt, sources = build_prompt_with_rag(req.message, history, req.use_rag)
    model_name = req.model or DEFAULT_MODEL

    def event_generator():
        full_response = ""
        start_t = time.time()
        token_count = 0

        # Send initial sources meta
        if sources:
            yield f"data: {json.dumps({'type': 'sources', 'sources': sources})}\n\n"

        try:
            res = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": model_name,
                    "prompt": prompt,
                    "stream": True,
                    "options": {"temperature": req.temperature}
                },
                stream=True,
                timeout=120
            )
            for line in res.iter_lines():
                if line:
                    chunk = json.loads(line.decode("utf-8"))
                    token = chunk.get("response", "")
                    full_response += token
                    token_count += 1
                    yield f"data: {json.dumps({'type': 'token', 'token': token})}\n\n"

                    if chunk.get("done", False):
                        elapsed = time.time() - start_t
                        tps = round(token_count / elapsed, 1) if elapsed > 0 else 0.0
                        add_message(req.session_id, "assistant", full_response, sources=sources, tokens_per_sec=tps)
                        yield f"data: {json.dumps({'type': 'done', 'tps': tps, 'full_response': full_response})}\n\n"
                        break
        except Exception as e:
            err_msg = f"[Device Manager Stream Error]: {str(e)}"
            add_message(req.session_id, "assistant", err_msg)
            yield f"data: {json.dumps({'type': 'error', 'message': err_msg})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.post("/api/documents/upload")
async def api_upload_document(file: UploadFile = File(...)):
    filename = file.filename
    filepath = os.path.join(UPLOAD_DIR, filename)
    
    content = await file.read()
    file_size = len(content)
    
    with open(filepath, "wb") as f:
        f.write(content)

    text_content = ""
    try:
        text_content = content.decode("utf-8", errors="ignore")
    except Exception:
        text_content = str(content)

    chunks = rag_engine.chunk_document(filename, filepath, text_content)
    doc_id = add_document(
        filename=filename,
        filepath=filepath,
        file_type=file.content_type or "text/plain",
        file_size=file_size,
        chunks_count=len(chunks)
    )

    return {
        "status": "success",
        "id": doc_id,
        "filename": filename,
        "file_size": file_size,
        "chunks": len(chunks)
    }

@app.get("/api/documents")
def api_get_documents():
    return get_documents()

@app.delete("/api/documents/{doc_id}")
def api_delete_document(doc_id: int):
    docs = get_documents()
    target = next((d for d in docs if d["id"] == doc_id), None)
    if target:
        rag_engine.remove_document_chunks(target["filename"])
        if os.path.exists(target["filepath"]):
            try:
                os.remove(target["filepath"])
            except Exception:
                pass
        delete_document(doc_id)
        return {"status": "success", "message": f"Document {doc_id} deleted"}
    raise HTTPException(status_code=404, detail="Document not found")

@app.post("/api/voice/command")
def api_voice_command(req: VoiceCommandRequest):
    return execute_voice_command(req.command)

if __name__ == "__main__":
    import uvicorn
    print("Starting Device Manager FastAPI Server on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
