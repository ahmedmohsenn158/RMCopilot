from infrastructure.audit_log import log_ai_suggestion
from infrastructure.groq_client import chat_completion, model_name
from infrastructure.vector_store import search_knowledge_base


async def rag_agent(state: dict) -> dict:
    docs = search_knowledge_base(state["message"], k=3)
    context = "\n\n".join(doc["text"] for doc in docs)
    sources = [doc["source"] for doc in docs]
    system = (
        "You are a banking knowledge assistant for Relationship Managers. Answer using only the "
        "context below. If the answer is not in the context, say so honestly.\n\n"
        f"CONTEXT:\n{context}"
    )
    reply = await chat_completion(system, state["message"])
    log_ai_suggestion(
        rm_id=state["rm_id"],
        customer_id=state.get("customer_id"),
        agent="rag_agent",
        suggestion=reply,
        model=model_name(),
    )
    return {**state, "reply": reply, "sources": sources, "agent_used": "rag_agent"}
