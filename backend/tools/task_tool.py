import os
from .base import ProposedAction, ToolResult
from infrastructure.audit_log import log_human_action


def create_task(
    title: str,
    due_date: str,       # "2026-06-29"
    customer_id: str,
    rm_id: str,
    priority: str = "medium",   # "low" | "medium" | "high"
) -> ProposedAction:
    return ProposedAction(
        tool="create_task",
        label="Create Task",
        summary=f"Create task: {title} due {due_date}",
        payload={
            "title": title,
            "due_date": due_date,
            "customer_id": customer_id,
            "rm_id": rm_id,
            "priority": priority,
        },
    )


async def execute_task(payload: dict, rm_id: str) -> ToolResult:
    try:
        result = await _adapter(payload)
        log_human_action(
            rm_id       = rm_id,
            customer_id = payload["customer_id"],
            action      = "approved",
            context     = f"Task created: {payload['title']} due {payload['due_date']}",
        )
        return result
    except Exception as exc:
        return ToolResult(success=False, message="Task creation failed", error=str(exc))


async def _adapter(payload: dict) -> ToolResult:
    provider = os.getenv("TASK_PROVIDER", "mock").lower()

    if provider == "salesforce":
        return await _salesforce_task(payload)

    # ── MOCK ──
    print(f"[Task mock] Would create: {payload['title']} by {payload['due_date']}")
    return ToolResult(
        success = True,
        message = f"Task created: {payload['title']} (mock)",
        data    = {"task_id": "mock-task-001"},
    )


async def _salesforce_task(payload: dict) -> ToolResult:
    from simple_salesforce import Salesforce  # type: ignore
    sf = Salesforce(
        username       = os.getenv("SF_USERNAME"),
        password       = os.getenv("SF_PASSWORD"),
        security_token = os.getenv("SF_TOKEN"),
    )
    result = sf.Task.create({
        "Subject":      payload["title"],
        "ActivityDate": payload["due_date"],
        "Priority":     payload["priority"].capitalize(),
        "Status":       "Not Started",
        "WhoId":        payload["customer_id"],
        "OwnerId":      payload["rm_id"],
    })
    return ToolResult(
        success = True,
        message = "Task created in Salesforce",
        data    = {"id": result["id"]},
    )