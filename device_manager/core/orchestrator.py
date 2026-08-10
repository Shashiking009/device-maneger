import time
from typing import Dict, Any, Optional
from core.intent_models import Intent, IntentType, RiskLevel, SpidyResponse
from core.intent_router import IntentRouter
from core.command_registry import CommandRegistry
from core.permission_manager import PermissionManager
from ai.qwen_engine import qwen_engine
from rag.rag_engine import rag_service
from database import add_message

from actions.planner import planner
from actions.executor import action_executor
from memory.context_manager import context_manager
from memory.memory_service import memory_service

class SpidyOrchestrator:
    """
    Central Decision-Making Entry Point for Spidy AI.
    Processes both text commands and voice inputs through a single unified pipeline:
    Input -> Normalize -> Context Resolution -> Action Planning -> Permission Check -> Command Execution -> SpidyResponse
    """
    def __init__(self):
        self.router = IntentRouter()
        self.registry = CommandRegistry()
        self.permission_mgr = PermissionManager()
        self.qwen = qwen_engine

    def process_command(self, user_input: str, session_id: Optional[str] = None, use_rag: bool = True) -> SpidyResponse:
        start_t = time.time()

        # 0a. Resolve Pronoun / Memory References ("Open my editor" -> "Open VS Code")
        user_input_resolved = context_manager.resolve_reference(user_input, session_id=session_id)

        # 0b. Multi-Step Action Planning check
        plan = planner.create_plan(user_input_resolved)
        if len(plan.actions) > 1:
            res_plan = action_executor.execute_plan(plan)
            latency_ms = round((time.time() - start_t) * 1000, 2)
            succ = res_plan.status.value == "COMPLETED"
            summary_msg = f"Executed {len(res_plan.actions)} actions: " + ", ".join([a.message for a in res_plan.actions if a.message])
            print(f"[ORCHESTRATOR LOG] input='{user_input}' | intent=MULTI_ACTION | steps={len(res_plan.actions)} | success={succ} | latency={latency_ms}ms")
            return SpidyResponse(
                success=succ,
                intent=IntentType.OPEN_APPLICATION,
                message=summary_msg,
                data={"plan_id": res_plan.plan_id, "steps": len(res_plan.actions)}
            )
        
        # 1. Route Intent
        intent = self.router.route(user_input_resolved)

        # 1b. Handle Memory Intents (MEMORY_SAVE, MEMORY_QUERY, MEMORY_DELETE, MEMORY_CLEAR)
        if intent.name in [IntentType.MEMORY_SAVE, IntentType.MEMORY_QUERY, IntentType.MEMORY_DELETE, IntentType.MEMORY_CLEAR]:
            if intent.name == IntentType.MEMORY_CLEAR and not intent.parameters.get("confirmed", False):
                return SpidyResponse(
                    success=False,
                    intent=intent.name,
                    message="This will delete all long-term memories. Confirm with 'Yes' to proceed.",
                    requires_confirmation=True
                )
            if intent.name == IntentType.MEMORY_CLEAR and intent.parameters.get("confirmed", False):
                from memory.storage import memory_storage
                memory_storage.clear_all_memories()
                return SpidyResponse(success=True, intent=intent.name, message="Cleared all saved memories.")

            succ, msg, data = memory_service.process_memory_command(user_input_resolved)
            return SpidyResponse(
                success=succ,
                intent=intent.name,
                message=msg,
                data=data or {}
            )

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
            if use_rag or intent.name == IntentType.RAG_QUERY:
                rag_res = rag_service.query(user_input)
                # If RAG returned relevant information or explicit grounded refusal
                if rag_res.sources or "couldn't find" in rag_res.answer:
                    reply = rag_res.answer
                    sources = [{"filename": s} for s in rag_res.sources]
                    tps = rag_res.tps or 0.0
                    latency_ms = round((time.time() - start_t) * 1000, 2)
                    print(f"[ORCHESTRATOR LOG] input='{user_input}' | intent=RAG_QUERY | confidence={intent.confidence} | success=True | latency={latency_ms}ms | tps={tps}")
                    
                    if session_id:
                        try:
                            add_message(session_id, "user", user_input)
                            add_message(session_id, "assistant", reply, sources=sources, tokens_per_sec=tps)
                        except Exception as e:
                            print("Database save error:", e)

                    return SpidyResponse(
                        success=True,
                        intent=IntentType.RAG_QUERY,
                        message=reply,
                        sources=sources,
                        tokens_per_sec=tps
                    )

            # Direct AI Question without local RAG context
            prompt = (
                "You are Device Manager, a privacy-first, on-device AI assistant powered by Qwen3 Small Language Model (SLM). "
                "You run entirely locally on the user's hardware. Provide clear, concise, and helpful answers.\n"
                f"User: {user_input}\nAssistant:"
            )

            reply, tps = self.qwen.generate_ai_response(prompt)
            latency_ms = round((time.time() - start_t) * 1000, 2)
            print(f"[ORCHESTRATOR LOG] input='{user_input}' | intent={intent.name.value} | confidence={intent.confidence} | success=True | latency={latency_ms}ms | tps={tps}")
            
            if session_id:
                try:
                    add_message(session_id, "user", user_input)
                    add_message(session_id, "assistant", reply, sources=[], tokens_per_sec=tps)
                except Exception as e:
                    print("Database save error:", e)

            return SpidyResponse(
                success=True,
                intent=intent.name,
                message=reply,
                sources=[],
                tokens_per_sec=tps
            )

        return SpidyResponse(
            success=False,
            intent=IntentType.UNKNOWN,
            message=f"Could not process input: '{user_input}'"
        )

orchestrator = SpidyOrchestrator()
