from fastapi import APIRouter
from pydantic import BaseModel, Field

from orchestrator.graph import run_agent

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    customer_id: str | None = None
    rm_id: str = "rm_sara_001"
    history: list[dict] = Field(default_factory=list)


class ChatResponse(BaseModel):
    reply: str
    sources: list[str] = Field(default_factory=list)
    agent_used: str


@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    result = await run_agent(
        message=req.message,
        customer_id=req.customer_id,
        rm_id=req.rm_id,
        history=req.history,
    )
    return ChatResponse(
        reply=result["reply"],
        sources=result.get("sources", []),
        agent_used=result.get("agent_used", "chatbot_agent"),
    )
