from pydantic import BaseModel, Field
from enum import Enum
from typing import Any
from datetime import datetime, timezone
import uuid


class ActionStatus(str, Enum):
    PENDING   = "pending"    # AI proposed it, waiting for RM approval
    APPROVED  = "approved"   # RM clicked approve
    REJECTED  = "rejected"   # RM dismissed it
    EXECUTED  = "executed"   # Side effect happened (email sent, CRM written)
    FAILED    = "failed"     # Execution attempt failed


class ProposedAction(BaseModel):
    """
    What the agent wants to do — shown to the RM for approval
    before any side effect happens.
    """
    action_id:   str         = Field(default_factory=lambda: str(uuid.uuid4()))
    tool:        str                          # "create_crm_note" | "send_email" | ...
    label:       str                          # Human-readable button label: "Push to CRM"
    summary:     str                          # One sentence shown in the UI
    payload:     dict[str, Any]               # Full args passed to execute()
    status:      ActionStatus = ActionStatus.PENDING
    created_at:  str          = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    executed_at: str | None   = None


class ToolResult(BaseModel):
    """
    Returned after a tool actually executes (post-approval).
    """
    success:     bool
    message:     str
    data:        dict[str, Any] = {}
    error:       str | None     = None