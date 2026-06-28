import json

from infrastructure.groq_client import chat_completion
from infrastructure.redis_client import get_recent_alerts


async def anomaly_agent(state: dict) -> dict:
    events = get_recent_alerts(state["customer_id"]) if state.get("customer_id") else []
    suspicious = [
        event
        for event in events
        if event.get("raw", {}).get("event_type") in ("transaction", "suspicious_pattern")
        and event.get("raw", {}).get("metadata", {}).get("deviation_multiplier", 1) > 3
    ]
    system = (
        "You are an anomaly detection agent for a bank RM. Explain suspicious transaction patterns "
        "in plain English. Include what happened, why it is unusual, and one clarifying question."
    )
    user = f"Suspicious events:\n{json.dumps(suspicious[:3], indent=2)}\n\nRM question: {state['message']}"
    reply = await chat_completion(system, user)
    return {**state, "reply": reply, "agent_used": "anomaly_agent"}
