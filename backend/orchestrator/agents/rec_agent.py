import json

from backend.infrastructure.groq_client import chat_completion
from backend.infrastructure.redis_client import get_recent_alerts
from backend.infrastructure.vector_store import search_knowledge_base


async def recommendation_agent(state: dict) -> dict:
    docs = search_knowledge_base(f"{state['message']} product eligibility pitch", k=3)
    alerts = get_recent_alerts(state["customer_id"]) if state.get("customer_id") else []
    product_context = "\n\n".join(doc["text"] for doc in docs)
    system = (
        "You are a product recommendation agent for a bank RM. Based on customer events and product "
        "knowledge, recommend relevant products and draft a short pitch script."
    )
    user = (
        f"Product knowledge:\n{product_context}\n\n"
        f"Customer events:\n{json.dumps(alerts[:4], indent=2)}\n\n"
        f"RM question: {state['message']}"
    )
    reply = await chat_completion(system, user)
    return {
        **state,
        "reply": reply,
        "sources": [doc["source"] for doc in docs],
        "agent_used": "recommendation_agent",
    }
