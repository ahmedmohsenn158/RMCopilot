import json

from backend.infrastructure.groq_client import chat_completion
from backend.infrastructure.redis_client import get_recent_alerts


async def alert_agent(state: dict) -> dict:
    alerts = get_recent_alerts(state["customer_id"]) if state.get("customer_id") else []
    system = (
        "You are an alert summarisation agent for a bank relationship manager. "
        "Summarise the most urgent alert and suggest one clear action. Be direct and brief."
    )
    user = f"Customer alerts:\n{json.dumps(alerts, indent=2)}\n\nRM question: {state['message']}"
    reply = await chat_completion(system, user)
    return {**state, "reply": reply, "agent_used": "alert_agent"}
