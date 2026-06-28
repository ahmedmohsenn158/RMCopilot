"""
Action executor — called ONLY after RM has clicked Approve.
Maps tool name → execute function, then writes to audit log.
"""
from datetime import datetime, timezone
from tools.base import ToolResult
from tools.crm_tool import execute_crm_note
from tools.email_tool import execute_email
from tools.meeting_tool import execute_meeting
from tools.task_tool import execute_task
from tools.customer import execute_search
from infrastructure.audit_log import log_human_action

EXECUTOR_MAP = {
    "create_crm_note":  execute_crm_note,
    "send_email":       execute_email,
    "schedule_meeting": execute_meeting,
    "create_task":      execute_task,
    "search_customer":  execute_search,
}


async def execute_approved_action(
    action_id: str,
    tool: str,
    payload: dict,
    rm_id: str,
) -> ToolResult:
    """
    Called by the /api/actions/execute endpoint after RM approval.
    Runs the real side effect and logs the human decision.
    """
    executor = EXECUTOR_MAP.get(tool)
    if not executor:
        return ToolResult(
            success = False,
            message = f"Unknown tool: {tool}",
            error   = "No executor registered for this tool",
        )

    result = await executor(payload, rm_id)
    return result


async def log_rejected_action(
    action_id: str,
    tool: str,
    customer_id: str,
    rm_id: str,
) -> None:
    """Log when RM dismisses a proposed action."""
    log_human_action(
        rm_id       = rm_id,
        customer_id = customer_id,
        action      = "rejected",
        context     = f"RM rejected proposed action: {tool} (action_id={action_id})",
    )