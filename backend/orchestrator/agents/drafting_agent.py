from infrastructure.audit_log import log_ai_suggestion
from infrastructure.groq_client import chat_completion, model_name


async def drafting_agent(state: dict) -> dict:
    system = (
        "You are a professional banking communications agent. Draft concise emails, call scripts, "
        "or CRM notes for Relationship Managers. Keep drafts under 150 words. Always end with: "
        "[Review before sending - do not send without RM approval]"
    )
    reply = await chat_completion(system, state["message"])
    log_ai_suggestion(
        rm_id=state["rm_id"],
        customer_id=state.get("customer_id"),
        agent="drafting_agent",
        suggestion=reply,
        model=model_name(),
    )
    return {**state, "reply": reply, "agent_used": "drafting_agent"}
