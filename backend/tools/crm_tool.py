import os
from datetime import datetime, timezone
from .base import ProposedAction, ToolResult
from infrastructure.audit_log import log_human_action


# ── Propose (AI side — no side effects) ─────────────────────────────────────

def create_crm_note(
    customer_id: str,
    rm_id: str,
    topic: str,
    outcome: str,
    action_items: list[str],
    next_steps: str,
) -> ProposedAction:
    """
    Build a ProposedAction for CRM note creation.
    Nothing is written until the RM approves.
    """
    return ProposedAction(
        tool    = "create_crm_note",
        label   = "Push to CRM",
        summary = f"Log call summary to CRM — topic: {topic}, outcome: {outcome}",
        payload = {
            "customer_id":  customer_id,
            "rm_id":        rm_id,
            "topic":        topic,
            "outcome":      outcome,
            "action_items": action_items,
            "next_steps":   next_steps,
        },
    )


# ── Execute (human approved — side effect happens here) ──────────────────────

async def execute_crm_note(payload: dict, rm_id: str) -> ToolResult:
    """
    Writes the CRM note. Tries real adapter first, falls back to mock.
    """
    try:
        result = await _adapter(payload)
        log_human_action(
            rm_id       = rm_id,
            customer_id = payload["customer_id"],
            action      = "approved",
            context     = f"CRM note pushed: {payload['topic']}",
        )
        return result
    except Exception as exc:
        return ToolResult(success=False, message="CRM write failed", error=str(exc))


async def _adapter(payload: dict) -> ToolResult:
    """
    Swap this body for your real CRM integration.

    Salesforce example:
        from simple_salesforce import Salesforce
        sf = Salesforce(
            username=os.getenv("SF_USERNAME"),
            password=os.getenv("SF_PASSWORD"),
            security_token=os.getenv("SF_TOKEN"),
        )
        sf.Task.create({
            "Subject":      payload["topic"],
            "Description":  payload["next_steps"],
            "WhoId":        payload["customer_id"],
            "OwnerId":      payload["rm_id"],
            "Status":       "Completed",
            "ActivityDate": datetime.now(timezone.utc).date().isoformat(),
        })

    HubSpot example:
        import hubspot
        client = hubspot.Client.create(access_token=os.getenv("HUBSPOT_TOKEN"))
        client.crm.objects.notes.basic_api.create(SimplePublicObjectInputForCreate(
            properties={"hs_note_body": payload["next_steps"], ...}
        ))

    For now: mock success so the demo works end-to-end.
    """
    crm_provider = os.getenv("CRM_PROVIDER", "mock").lower()

    if crm_provider == "salesforce":
        return await _salesforce_adapter(payload)
    if crm_provider == "hubspot":
        return await _hubspot_adapter(payload)

    # ── MOCK ──
    print(f"[CRM mock] Would write: {payload}")
    return ToolResult(
        success = True,
        message = "CRM note created (mock)",
        data    = {"note_id": "mock-note-001", "provider": "mock"},
    )


async def _salesforce_adapter(payload: dict) -> ToolResult:
    # Install: pip install simple-salesforce
    from simple_salesforce import Salesforce  # type: ignore
    sf = Salesforce(
        username       = os.getenv("SF_USERNAME"),
        password       = os.getenv("SF_PASSWORD"),
        security_token = os.getenv("SF_TOKEN"),
    )
    result = sf.Task.create({
        "Subject":      payload["topic"],
        "Description":  f"Outcome: {payload['outcome']}\nNext: {payload['next_steps']}",
        "Status":       "Completed",
        "ActivityDate": datetime.now(timezone.utc).date().isoformat(),
    })
    return ToolResult(
        success = True,
        message = "CRM note created in Salesforce",
        data    = {"id": result["id"]},
    )


async def _hubspot_adapter(payload: dict) -> ToolResult:
    # Install: pip install hubspot-api-client
    import hubspot  # type: ignore
    from hubspot.crm.objects.notes import SimplePublicObjectInputForCreate  # type: ignore
    client = hubspot.Client.create(access_token=os.getenv("HUBSPOT_TOKEN"))
    result = client.crm.objects.notes.basic_api.create(
        SimplePublicObjectInputForCreate(properties={
            "hs_note_body":      payload["next_steps"],
            "hs_timestamp":      str(int(datetime.now(timezone.utc).timestamp() * 1000)),
        })
    )
    return ToolResult(
        success = True,
        message = "CRM note created in HubSpot",
        data    = {"id": result.id},
    )