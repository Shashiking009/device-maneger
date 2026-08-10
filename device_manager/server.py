import os
import json
import uuid
import time
import requests
from typing import List, Dict, Any, Optional, Tuple
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks, Query, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from telemetry import get_system_telemetry, SystemStats
from events import event_bus, SpidyEvent

from database import init_db, create_session, get_sessions, get_session_messages, add_message, add_document, get_documents, delete_document, delete_session
from voice_assistant import execute_voice_command
from config import HOST, PORT, OLLAMA_HOST, OLLAMA_MODEL, UPLOAD_DIR
from core.orchestrator import orchestrator
from rag.rag_engine import rag_service
from rag.models import RAGQueryResponse, RAGStatusResponse

OLLAMA_URL = OLLAMA_HOST
DEFAULT_MODEL = OLLAMA_MODEL
UPLOAD_DIR = str(UPLOAD_DIR)

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
    resp = orchestrator.process_command(req.message, session_id=req.session_id, use_rag=req.use_rag)
    return {
        "role": "assistant",
        "content": resp.message,
        "intent": resp.intent.value,
        "sources": resp.sources or [],
        "tokens_per_sec": resp.tokens_per_sec or 0.0,
        "model": req.model or DEFAULT_MODEL
    }

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

    idx_res = rag_service.index(filepath)
    doc_id = add_document(
        filename=filename,
        filepath=filepath,
        file_type=file.content_type or "text/plain",
        file_size=file_size,
        chunks_count=idx_res.get("chunks_count", 0)
    )

    return {
        "status": "success",
        "id": doc_id,
        "filename": filename,
        "file_size": file_size,
        "chunks": idx_res.get("chunks_count", 0),
        "indexing": idx_res
    }

@app.get("/api/documents")
def api_get_documents():
    return get_documents()

@app.delete("/api/documents/{doc_id}")
def api_delete_document(doc_id: int):
    docs = get_documents()
    target = next((d for d in docs if d["id"] == doc_id), None)
    if target:
        rag_service.remove(target["filepath"])
        if os.path.exists(target["filepath"]):
            try:
                os.remove(target["filepath"])
            except Exception:
                pass
        delete_document(doc_id)
        return {"status": "success", "message": f"Document {doc_id} deleted"}
    raise HTTPException(status_code=404, detail="Document not found")

# --- STANDARDIZED RAG API ENDPOINTS ---

class RAGIndexRequest(BaseModel):
    path: str

class RAGQueryApiRequest(BaseModel):
    query: str
    top_k: int = 5

@app.post("/api/rag/index")
def api_rag_index(req: RAGIndexRequest):
    return rag_service.index(req.path)

@app.post("/api/rag/reindex")
def api_rag_reindex(req: RAGIndexRequest):
    return rag_service.reindex(req.path)

@app.post("/api/rag/query", response_model=RAGQueryResponse)
def api_rag_query(req: RAGQueryApiRequest):
    return rag_service.query(req.query, top_k=req.top_k)

@app.delete("/api/rag/document")
def api_rag_delete_doc(req: RAGIndexRequest):
    success = rag_service.remove(req.path)
    return {"status": "success" if success else "error", "path": req.path}

@app.post("/api/rag/clear")
def api_rag_clear():
    rag_service.clear()
    return {"status": "success", "message": "Local RAG index cleared"}

@app.get("/api/rag/status", response_model=RAGStatusResponse)
def api_rag_status():
    return rag_service.status()

from voice.voice_manager import voice_manager
from voice.voice_state import voice_state_machine
from voice.text_to_speech import tts_engine

@app.get("/api/voice/status")
def api_voice_status():
    return {
        "state": voice_state_machine.current_state.value,
        "is_speaking": tts_engine.is_speaking
    }

@app.post("/api/voice/stop")
def api_voice_stop():
    tts_engine.stop()
    return {"status": "success", "message": "Voice playback stopped"}

@app.post("/api/voice/command")
def api_voice_command(req: VoiceCommandRequest):
    return voice_manager.process_voice_text(req.command)

# --- LOCAL MEMORY API ENDPOINTS ---

from memory.models import Memory, MemoryCategory, MemorySource
from memory.storage import memory_storage

class MemorySaveRequest(BaseModel):
    key: str
    value: str
    category: str = "PREFERENCE"

@app.get("/api/memory")
def api_get_memories(category: Optional[str] = None):
    cat_enum = None
    if category:
        try:
            cat_enum = MemoryCategory(category.upper())
        except Exception:
            pass
    memories = memory_storage.list_memories(cat_enum)
    return {"memories": [m.model_dump() for m in memories]}

@app.post("/api/memory")
def api_save_memory(req: MemorySaveRequest):
    cat_enum = MemoryCategory.PREFERENCE
    if hasattr(MemoryCategory, req.category.upper()):
        cat_enum = MemoryCategory(req.category.upper())

    mem = Memory(
        category=cat_enum,
        key=req.key,
        value=req.value,
        source=MemorySource.EXPLICIT_USER
    )
    succ, msg, stored_mem = memory_storage.save_memory(mem)
    if not succ:
        raise HTTPException(status_code=400, detail=msg)
    return {"status": "success", "message": msg, "memory": stored_mem.model_dump() if stored_mem else None}

@app.delete("/api/memory/{key_or_id}")
def api_delete_memory(key_or_id: str):
    succ = memory_storage.delete_memory(key_or_id)
    if not succ:
        raise HTTPException(status_code=404, detail=f"Memory '{key_or_id}' not found")
    return {"status": "success", "message": f"Deleted memory '{key_or_id}'"}

@app.post("/api/memory/clear")
def api_clear_memories():
    memory_storage.clear_all_memories()
    return {"status": "success", "message": "All saved memories cleared"}

# --- SYSTEM TELEMETRY & WEBSOCKET EVENT STREAM ---

@app.get("/api/system", response_model=SystemStats)
def api_system_telemetry():
    return get_system_telemetry()

@app.websocket("/ws/spidy")
async def websocket_spidy(websocket: WebSocket):
    await websocket.accept()
    event_bus.register_ws(websocket)
    
    # Send initial READY event
    await websocket.send_json({
        "event_type": "SYSTEM_READY",
        "state": voice_state_machine.current_state.value,
        "timestamp": time.time(),
        "message": "Connected to Spidy AI WebSocket stream."
    })
    
    try:
        while True:
            # Keep connection alive & handle incoming pings
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_json({"event_type": "PONG", "timestamp": time.time()})
    except WebSocketDisconnect:
        event_bus.unregister_ws(websocket)
    except Exception:
        event_bus.unregister_ws(websocket)

if __name__ == "__main__":
    import uvicorn
    print(f"Starting Device Manager FastAPI Server on http://{HOST}:{PORT}")
    uvicorn.run(app, host=HOST, port=PORT)
