"""
All 7 agents. Each receives AgentState, returns updated state with:
  - reply:            str          (shown immediately in UI)
  - proposed_actions: list[dict]   (actions waiting for RM approval)
"""
import json
import os
from infrastructure.audit_log import log_ai_suggestion
from infrastructure.redis_client import get_recent_alerts
from tools.crm_tool import create_crm_note
from tools.email_tool import send_email
from tools.task_tool import create_task

# Shared LLM client (Groq)
async def _llm(system: str, user: str) -> str:
    from infrastructure.llm_client import chat_completion
    return await chat_completion(system=system, user=user)


def _serialise(actions) -> list[dict]:
    return [a.model_dump() for a in actions]


# ── 1. CHATBOT AGENT ─────────────────────────────────────────────────────────

async def chatbot_agent(state: dict) -> dict:
    history_text = "\n".join(
        f"{m['role'].upper()}: {m.get('text', '')}"
        for m in state.get("history", [])[-6:]
    )
    system = f"""You are an AI assistant for bank Relationship Managers.
Help with customer questions, bank processes, product knowledge,
and onboarding guidance for new RMs. Be concise and practical.

Conversation history:
{history_text}"""

    reply = await _llm(system, state["message"])
    log_ai_suggestion(state["rm_id"], state.get("customer_id"), "chatbot_agent", reply, "groq")

    return {**state, "reply": reply, "proposed_actions": [], "agent_used": "chatbot_agent"}


# ── 2. RAG AGENT ─────────────────────────────────────────────────────────────

async def rag_agent(state: dict) -> dict:
    try:
        from infrastructure.vector_store import load_vector_store
        vs = load_vector_store()
        docs = vs.similarity_search(state["message"], k=3)
        context = "\n\n".join(d.page_content for d in docs)
        sources = [d.metadata.get("source", "") for d in docs]
    except Exception:
        context = "Knowledge base not yet indexed."
        sources = []

    system = f"""You are a banking knowledge assistant for Relationship Managers.
Answer using only the context below. Be concise and practical.
If the answer is not in the context, say so honestly.

CONTEXT:
{context}"""

    reply = await _llm(system, state["message"])
    log_ai_suggestion(state["rm_id"], state.get("customer_id"), "rag_agent", reply, "groq")

    return {**state, "reply": reply, "sources": sources,
            "proposed_actions": [], "agent_used": "rag_agent"}


# ── 3. ALERT AGENT ───────────────────────────────────────────────────────────

async def alert_agent(state: dict) -> dict:
    customer_id = state.get("customer_id")
    alerts = get_recent_alerts(customer_id) if customer_id else []
    alerts_text = json.dumps(alerts[:5], indent=2) if alerts else "No active alerts."

    system = """You are an alert summarisation agent for a bank RM.
Given the customer's active alerts, summarise the most urgent one
and suggest one clear action. Be direct — the RM is on a live call."""

    reply = await _llm(system, f"Alerts:\n{alerts_text}\n\nRM question: {state['message']}")

    # Propose a CRM task if there's a breach
    proposed = []
    breach = next((a for a in alerts if a.get("event_type") == "credit_limit_breach"), None)
    if breach and customer_id:
        proposed.append(create_crm_note(
            customer_id  = customer_id,
            rm_id        = state["rm_id"],
            topic        = "Credit limit breach",
            outcome      = "Discussed with customer",
            action_items = ["Notify credit team", "Log explanation from customer"],
            next_steps   = "Await credit team review within 24 hours",
        ))

    log_ai_suggestion(state["rm_id"], customer_id, "alert_agent", reply, "groq")

    return {**state, "reply": reply,
            "proposed_actions": _serialise(proposed), "agent_used": "alert_agent"}


# ── 4. RECOMMENDATION AGENT ──────────────────────────────────────────────────

async def recommendation_agent(state: dict) -> dict:
    customer_id = state.get("customer_id")
    alerts = get_recent_alerts(customer_id) if customer_id else []

    try:
        from infrastructure.vector_store import load_vector_store
        vs = load_vector_store()
        docs = vs.similarity_search("product eligibility pitch " + state["message"], k=3)
        product_context = "\n\n".join(d.page_content for d in docs)
    except Exception:
        product_context = "Product catalogue not indexed yet."

    system = f"""You are a product recommendation agent for a bank RM.
Recommend the most relevant product and draft a 2-sentence pitch script.

Product knowledge:
{product_context}

Recent customer events:
{json.dumps(alerts[:3], indent=2)}"""

    reply = await _llm(system, state["message"])

    # Propose a follow-up task to send the product sheet
    proposed = []
    if customer_id:
        proposed.append(create_task(
            title       = "Send product information sheet to customer",
            due_date    = "2026-06-30",
            customer_id = customer_id,
            rm_id       = state["rm_id"],
            priority    = "high",
        ))

    log_ai_suggestion(state["rm_id"], customer_id, "recommendation_agent", reply, "groq")

    return {**state, "reply": reply,
            "proposed_actions": _serialise(proposed), "agent_used": "recommendation_agent"}


# ── 5. DRAFTING AGENT ────────────────────────────────────────────────────────

async def drafting_agent(state: dict) -> dict:
    customer_id    = state.get("customer_id")
    customer_name  = state.get("customer_name",  "Customer")
    customer_email = state.get("customer_email", "")   # passed from LiveCallPage context

    system = """You are a professional banking communications agent.
Draft concise, professional follow-up emails for Relationship Managers.
Keep emails under 150 words. Use formal but warm tone.
End with: Warm regards,\nSara Hassan
Do NOT add any approval reminders — the system handles that."""

    reply = await _llm(system, state["message"])

    proposed = []
    if customer_id:
        # Only propose email send if we have a real address
        if customer_email:
            proposed.append(send_email(
                to_name      = customer_name,
                to_email     = customer_email,
                subject      = "Follow-up from today's call",
                body         = reply,
                rm_id        = state["rm_id"],
                customer_id  = customer_id,
            ))
        else:
            # No email on file — tell the RM
            reply += "\n\n⚠️ No email address on file for this customer. Add one to send directly."

        proposed.append(create_crm_note(
            customer_id  = customer_id,
            rm_id        = state["rm_id"],
            topic        = "Follow-up email drafted",
            outcome      = "Email pending RM approval",
            action_items = ["Send follow-up email"],
            next_steps   = "Await customer response",
        ))

    log_ai_suggestion(state["rm_id"], customer_id, "drafting_agent", reply, "groq")

    return {**state, "reply": reply,
            "proposed_actions": _serialise(proposed), "agent_used": "drafting_agent"}


# ── 6. ANALYTICS AGENT ───────────────────────────────────────────────────────

async def analytics_agent(state: dict) -> dict:
    system = """You are a portfolio analytics agent for a bank RM.
Provide clear, actionable bullet-point insights about the RM's client portfolio.
Focus on: upcoming renewals, at-risk accounts, cross-sell opportunities,
and performance trends. Be brief and specific."""

    reply = await _llm(system, state["message"])
    log_ai_suggestion(state["rm_id"], state.get("customer_id"), "analytics_agent", reply, "groq")

    return {**state, "reply": reply,
            "proposed_actions": [], "agent_used": "analytics_agent"}


# ── 7. ANOMALY DETECTION AGENT ───────────────────────────────────────────────

async def anomaly_agent(state: dict) -> dict:
    customer_id = state.get("customer_id")
    events = get_recent_alerts(customer_id) if customer_id else []

    suspicious = [
        e for e in events
        if e.get("event_type") in ("transaction", "suspicious_pattern")
        and e.get("metadata", {}).get("deviation_multiplier", 1) > 3
    ]
    events_text = json.dumps(suspicious[:3], indent=2) if suspicious else "No anomalous events."

    system = """You are an anomaly detection agent for a bank RM.
Write a 2-sentence plain-English explanation of the anomaly.
Include: what happened, how unusual it is (e.g. "18x above average"),
and one clarifying question the RM can ask the customer.
Do NOT use ML jargon."""

    reply = await _llm(
        system,
        f"Suspicious events:\n{events_text}\n\nRM question: {state['message']}"
    )

    # Propose a CRM note to log the anomaly review
    proposed = []
    if suspicious and customer_id:
        proposed.append(create_crm_note(
            customer_id  = customer_id,
            rm_id        = state["rm_id"],
            topic        = "Anomalous transaction review",
            outcome      = "Under review",
            action_items = ["Clarify purpose with customer", "Escalate to compliance if unexplained"],
            next_steps   = "Log customer explanation and escalate if necessary",
        ))

    log_ai_suggestion(state["rm_id"], customer_id, "anomaly_agent", reply, "groq")

    return {**state, "reply": reply,
            "proposed_actions": _serialise(proposed), "agent_used": "anomaly_agent"}