import time
from typing import Dict, Any, Optional
from core.intent_models import Intent, IntentType, RiskLevel, SpidyResponse
from core.intent_router import IntentRouter
from core.command_registry import CommandRegistry
from core.permission_manager import PermissionManager
from ai.qwen_engine import qwen_engine
from rag_engine import rag_engine
from database import add_message

class SpidyOrchestrator:
    """
    Central Decision-Making Entry Point for Spidy AI.
    Processes both text commands and voice inputs through a single unified pipeline:
    Input -> Normalize -> Deterministic Intent Detection -> (Qwen Fallback) -> Permission Check -> Command Execution -> SpidyResponse
    """
    def __init__(self):
        self.router = IntentRouter()
        self.registry = CommandRegistry()
        self.permission_mgr = PermissionManager()
        self.qwen = qwen_engine

    def process_command(self, user_input: str, session_id: Optional[str] = None, use_rag: bool = True) -> SpidyResponse:
        start_t = time.time()
        
        # 1. Route Intent
        intent = self.router.route(user_input)

        # 2. Risk & Permission Check
        self.permission_mgr.assess_risk(intent)
        if not self.permission_mgr.is_permitted(intent):
            return SpidyResponse(
                success=False,
                intent=intent.name,
                message=f"Action '{intent.name.value}' is blocked by security policy."
            )

        # 3. Execute Registered System Automation Handler
        if intent.name in self.registry.handlers:
            resp = self.registry.execute(intent)
            latency_ms = round((time.time() - start_t) * 1000, 2)
            print(f"[ORCHESTRATOR LOG] input='{user_input}' | intent={intent.name.value} | confidence={intent.confidence} | success={resp.success} | latency={latency_ms}ms")
            
            if session_id:
                try:
                    add_message(session_id, "user", user_input)
                    add_message(session_id, "assistant", resp.message)
                except Exception as e:
                    print("Database save error:", e)
            return resp

        # 4. Handle AI Questions & Local RAG Queries
        if intent.name in [IntentType.AI_QUESTION, IntentType.RAG_QUERY, IntentType.UNKNOWN]:
            sources = []
            rag_context = ""
            if use_rag:
                search_results = rag_engine.search(user_input, top_k=3)
                if search_results:
                    sources = search_results
                    rag_context = "\n\n[RELEVANT LOCAL KNOWLEDGE BASE CONTEXT]:\n"
                    for idx, item in enumerate(search_results, 1):
                        rag_context += f"--- Source {idx} ({item['filename']}) ---\n{item['snippet']}\n"
                    rag_context += "--- END CONTEXT ---\nPlease incorporate relevant details from above context if helpful.\n"

            prompt = (
                "You are Device Manager, a privacy-first, on-device AI assistant powered by Qwen3 Small Language Model (SLM). "
                f"You run entirely locally on the user's hardware. Provide clear, concise, and helpful answers.\n{rag_context}\n"
                f"User: {user_input}\nAssistant:"
            )

            reply, tps = self.qwen.generate_ai_response(prompt)
            latency_ms = round((time.time() - start_t) * 1000, 2)
            print(f"[ORCHESTRATOR LOG] input='{user_input}' | intent={intent.name.value} | confidence={intent.confidence} | success=True | latency={latency_ms}ms | tps={tps}")
            
            if session_id:
                try:
                    add_message(session_id, "user", user_input)
                    add_message(session_id, "assistant", reply, sources=sources, tokens_per_sec=tps)
                except Exception as e:
                    print("Database save error:", e)

            return SpidyResponse(
                success=True,
                intent=intent.name,
                message=reply,
                sources=sources,
                tokens_per_sec=tps
            )

        return SpidyResponse(
            success=False,
            intent=IntentType.UNKNOWN,
            message=f"Could not process input: '{user_input}'"
        )

orchestrator = SpidyOrchestrator()
