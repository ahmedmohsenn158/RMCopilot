from backend.infrastructure.groq_client import chat_completion


async def chatbot_agent(state: dict) -> dict:
    history_text = "\n".join(
        f"{m.get('role', 'user').upper()}: {m.get('text', m.get('content', ''))}"
        for m in state.get("history", [])[-6:]
    )
    system = (
        "You are an AI assistant for bank Relationship Managers. Help with customer context, "
        "bank processes, product knowledge, and onboarding. Be concise, practical, and professional."
    )
    user = f"Conversation history:\n{history_text}\n\nCurrent question: {state['message']}"
    reply = await chat_completion(system, user)
    return {**state, "reply": reply, "agent_used": "chatbot_agent"}
