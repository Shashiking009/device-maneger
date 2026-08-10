from typing import List, Tuple
from rag.models import SearchResult

RAG_SYSTEM_PROMPT = """You are Spidy AI's local document assistant.
Your job is to answer the user's question using ONLY the supplied local document context below.

CRITICAL INSTRUCTIONS:
1. Base your answer STRICTLY on the provided document excerpts.
2. Mention the source filenames (e.g. Sources: • filename.md) when citing facts.
3. If the answer is NOT present in the provided context, state clearly: "I couldn't find relevant information in your indexed documents."
4. Do NOT invent facts or hallucinate details outside the supplied excerpts.
"""

def build_rag_prompt(question: str, search_results: List[SearchResult]) -> Tuple[str, List[str]]:
    if not search_results:
        return "", []

    context_str = "\n[SUPPLIED LOCAL DOCUMENT CONTEXT]:\n"
    unique_sources = []
    seen_filenames = set()

    for res in search_results:
        if res.filename not in seen_filenames:
            seen_filenames.add(res.filename)
            unique_sources.append(res.filename)

        context_str += f"\n--- SOURCE: {res.filename} (Score: {res.score:.2f}) ---\n{res.content}\n"

    context_str += "\n--- END CONTEXT ---\n"

    full_prompt = f"{RAG_SYSTEM_PROMPT}\n{context_str}\nUser Question: {question}\nAssistant:"
    return full_prompt, unique_sources
