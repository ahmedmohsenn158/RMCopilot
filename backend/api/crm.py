from fastapi import APIRouter
from pydantic import BaseModel, Field
from backend.infrastructure.audit_log import log_human_action

router = APIRouter()

class CRMUpdateRequest(BaseModel):
    customer_id: str = "cust_khaled_001"
    rm_id: str = "rm_sara_001"
    topic: str = "Credit line + FX hedging"
    outcome: str = "Positive - follow up"
    action_items: list[str] = Field(default_factory=list)
    next_steps: str = "Trade finance review"


@router.post("/update")
def push_crm_update(req: CRMUpdateRequest) -> dict:
    log_human_action(
        rm_id=req.rm_id,
        customer_id=req.customer_id,
        action="approved",
        context=f"CRM update: {req.topic} / {req.outcome}",
    )
    return {"success": True, "message": "CRM updated (mock)"}
