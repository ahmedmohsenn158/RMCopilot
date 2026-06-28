from fastapi import APIRouter
from pydantic import BaseModel
from backend.orchestrator.graph import run_agent

router = APIRouter()


class ChatRequest(BaseModel):
    message:        str
    customer_id:    str | None = None
    customer_name:  str | None = None   # ← NEW: passed from frontend
    customer_email: str | None = None   # ← NEW: real email for sending
    rm_id:          str
    history:        list[dict] = []


class ChatResponse(BaseModel):
    reply:            str
    proposed_actions: list[dict] = []
    sources:          list[str]  = []
    agent_used:       str        = ""


@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest):
    result = await run_agent(
        message        = req.message,
        customer_id    = req.customer_id,
        customer_name  = req.customer_name,
        customer_email = req.customer_email,
        rm_id          = req.rm_id,
        history        = req.history,
    )
    return ChatResponse(
        reply            = result["reply"],
        proposed_actions = result.get("proposed_actions", []),
        sources          = result.get("sources", []),
        agent_used       = result.get("agent_used", ""),
    )