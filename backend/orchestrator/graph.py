"""
LangGraph orchestrator — routes messages to agents,
returns structured {reply, proposed_actions} instead of plain text.
"""
from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal
from tools.base import ProposedAction


class AgentState(TypedDict):
    message:          str
    customer_id:      str | None
    customer_name:    str | None   # ← NEW
    customer_email:   str | None   # ← NEW
    rm_id:            str
    history:          list[dict]
    customer_data:    dict | None
    reply:            str
    proposed_actions: list[dict]
    sources:          list[str]
    agent_used:       str
    route:            str


# ── Router ────────────────────────────────────────────────────────────────────

def _router(state: AgentState) -> Literal[
    "rag_agent", "alert_agent", "recommendation_agent",
    "drafting_agent", "chatbot_agent", "analytics_agent", "anomaly_agent"
]:
    msg = state["message"].lower()

    if any(k in msg for k in ["anomaly", "unusual", "suspicious", "flag"]):
        return "anomaly_agent"
    if any(k in msg for k in ["alert", "breach", "limit", "expir"]):
        return "alert_agent"
    if any(k in msg for k in ["recommend", "product", "eligible", "pitch", "sell"]):
        return "recommendation_agent"
    if any(k in msg for k in ["draft", "email", "write", "follow", "crm", "note", "send"]):
        return "drafting_agent"
    if any(k in msg for k in ["analytics", "portfolio", "performance", "trend"]):
        return "analytics_agent"
    if any(k in msg for k in ["policy", "process", "how do", "what is", "procedure", "new rm"]):
        return "rag_agent"

    return "chatbot_agent"


def _route_node(state: AgentState) -> AgentState:
    return {**state, "route": _router(state)}


# ── Import agents lazily to avoid circular imports ────────────────────────────

def _get_agents():
    from orchestrator.agents import (
        rag_agent, alert_agent, recommendation_agent,
        drafting_agent, chatbot_agent, analytics_agent, anomaly_agent,
    )
    return {
        "rag_agent":            rag_agent,
        "alert_agent":          alert_agent,
        "recommendation_agent": recommendation_agent,
        "drafting_agent":       drafting_agent,
        "chatbot_agent":        chatbot_agent,
        "analytics_agent":      analytics_agent,
        "anomaly_agent":        anomaly_agent,
    }


def build_graph():
    agents = _get_agents()
    g = StateGraph(AgentState)

    g.add_node("router_node", _route_node)
    for name, fn in agents.items():
        g.add_node(name, fn)

    g.set_entry_point("router_node")
    g.add_conditional_edges(
        "router_node",
        lambda s: s["route"],
        {name: name for name in agents},
    )
    for name in agents:
        g.add_edge(name, END)

    return g.compile()


graph = build_graph()


async def run_agent(
    message: str,
    customer_id: str | None,
    rm_id: str,
    history: list[dict],
    customer_name: str | None = None,
    customer_email: str | None = None,
) -> dict:
    result = await graph.ainvoke({
        "message":          message,
        "customer_id":      customer_id,
        "customer_name":    customer_name,
        "customer_email":   customer_email,
        "rm_id":            rm_id,
        "history":          history,
        "customer_data":    None,
        "reply":            "",
        "proposed_actions": [],
        "sources":          [],
        "agent_used":       "",
        "route":            "",
    })
    return {
        "reply":            result["reply"],
        "proposed_actions": result["proposed_actions"],
        "sources":          result.get("sources", []),
        "agent_used":       result.get("agent_used", ""),
    }