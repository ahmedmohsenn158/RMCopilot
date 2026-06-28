from infrastructure.data_access import load_events
from infrastructure.groq_client import chat_completion


async def analytics_agent(state: dict) -> dict:
    events = load_events()
    system = (
        "You are a portfolio analytics agent for a bank RM. Provide concise, actionable insights "
        "about renewals, at-risk accounts, cross-sell opportunities, and suspicious activity."
    )
    user = f"Portfolio event count: {len(events)}\nRM question: {state['message']}"
    reply = await chat_completion(system, user)
    return {**state, "reply": reply, "agent_used": "analytics_agent"}
