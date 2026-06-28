"""
/api/actions/ — the human-approval gate.

Two endpoints:
  POST /api/actions/execute  ← RM clicked Approve
  POST /api/actions/reject   ← RM clicked Dismiss
"""
from fastapi import APIRouter
from pydantic import BaseModel
from tools.executor import execute_approved_action, log_rejected_action
from tools.base import ToolResult

router = APIRouter()


class ExecuteRequest(BaseModel):
    action_id:   str
    tool:        str
    payload:     dict
    rm_id:       str
    customer_id: str | None = None


class RejectRequest(BaseModel):
    action_id:   str
    tool:        str
    rm_id:       str
    customer_id: str | None = None


@router.post("/execute", response_model=ToolResult)
async def execute_action(req: ExecuteRequest):
    """
    Called when RM clicks Approve on a proposed action.
    This is the only place real side effects happen.
    """
    return await execute_approved_action(
        action_id = req.action_id,
        tool      = req.tool,
        payload   = req.payload,
        rm_id     = req.rm_id,
    )


@router.post("/reject")
async def reject_action(req: RejectRequest):
    """
    Called when RM clicks Dismiss on a proposed action.
    Logs the rejection — no side effects.
    """
    await log_rejected_action(
        action_id   = req.action_id,
        tool        = req.tool,
        customer_id = req.customer_id or "",
        rm_id       = req.rm_id,
    )
    return {"success": True, "message": "Action dismissed and logged"}