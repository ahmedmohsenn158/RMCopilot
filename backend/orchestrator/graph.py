from typing import Literal, TypedDict

from orchestrator.agents.alert_agent import alert_agent
from orchestrator.agents.analytics_agent import analytics_agent
from orchestrator.agents.anomaly_agent import anomaly_agent
from orchestrator.agents.chatbot_agent import chatbot_agent
from orchestrator.agents.drafting_agent import drafting_agent
from orchestrator.agents.rag_agent import rag_agent
from orchestrator.agents.rec_agent import recommendation_agent


class AgentState(TypedDict):
    message: str
    customer_id: str | None
    rm_id: str
    history: list[dict]
    reply: str
    sources: list[str]
    agent_used: str
    route: str


Route = Literal[
    "rag_agent",
    "alert_agent",
    "recommendation_agent",
    "drafting_agent",
    "chatbot_agent",
    "analytics_agent",
    "anomaly_agent",
]


def router(state: AgentState) -> Route:
    msg = state["message"].lower()
    if any(k in msg for k in ["anomaly", "unusual", "suspicious", "flag"]):
        return "anomaly_agent"
    if any(k in msg for k in ["alert", "breach", "limit", "expir"]):
        return "alert_agent"
    if any(k in msg for k in ["recommend", "product", "eligible", "pitch", "sell", "fx"]):
        return "recommendation_agent"
    if any(k in msg for k in ["draft", "email", "write", "follow", "crm", "note", "script"]):
        return "drafting_agent"
    if any(k in msg for k in ["analytics", "portfolio", "performance", "trend"]):
        return "analytics_agent"
    if any(k in msg for k in ["policy", "process", "how do", "what is", "procedure", "new"]):
        return "rag_agent"
    return "chatbot_agent"


async def run_agent(message: str, customer_id: str | None, rm_id: str, history: list[dict]) -> dict:
    state: AgentState = {
        "message": message,
        "customer_id": customer_id,
        "rm_id": rm_id,
        "history": history,
        "reply": "",
        "sources": [],
        "agent_used": "",
        "route": "",
    }
    route = router(state)
    state["route"] = route

    handlers = {
        "rag_agent": rag_agent,
        "alert_agent": alert_agent,
        "recommendation_agent": recommendation_agent,
        "drafting_agent": drafting_agent,
        "chatbot_agent": chatbot_agent,
        "analytics_agent": analytics_agent,
        "anomaly_agent": anomaly_agent,
    }
    return await handlers[route](state)
