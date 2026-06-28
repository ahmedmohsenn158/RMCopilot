import os
from .base import ProposedAction, ToolResult
from infrastructure.audit_log import log_human_action


# ── Propose ──────────────────────────────────────────────────────────────────

def schedule_meeting(
    customer_name: str,
    customer_email: str,
    topic: str,
    proposed_datetime: str,   # ISO 8601 e.g. "2026-06-30T10:00:00"
    duration_minutes: int,
    rm_id: str,
    customer_id: str,
) -> ProposedAction:
    return ProposedAction(
        tool    = "schedule_meeting",
        label   = "Schedule Meeting",
        summary = f"Schedule {duration_minutes}-min meeting with {customer_name} on {proposed_datetime[:10]}",
        payload = {
            "customer_name":      customer_name,
            "customer_email":     customer_email,
            "topic":              topic,
            "proposed_datetime":  proposed_datetime,
            "duration_minutes":   duration_minutes,
            "rm_id":              rm_id,
            "customer_id":        customer_id,
        },
    )


# ── Execute ───────────────────────────────────────────────────────────────────

async def execute_meeting(payload: dict, rm_id: str) -> ToolResult:
    try:
        result = await _adapter(payload)
        log_human_action(
            rm_id       = rm_id,
            customer_id = payload["customer_id"],
            action      = "approved",
            context     = f"Meeting scheduled with {payload['customer_name']} at {payload['proposed_datetime']}",
        )
        return result
    except Exception as exc:
        return ToolResult(success=False, message="Meeting scheduling failed", error=str(exc))


async def _adapter(payload: dict) -> ToolResult:
    """
    Swap body for your real calendar provider.

    Microsoft Graph (Outlook Calendar):
        POST https://graph.microsoft.com/v1.0/me/events
        body = { "subject": topic, "start": {...}, "end": {...},
                 "attendees": [{"emailAddress": {"address": customer_email}}] }

    Google Calendar:
        service.events().insert(calendarId="primary", body={...}).execute()
    """
    provider = os.getenv("CALENDAR_PROVIDER", "mock").lower()

    if provider == "graph":
        return await _graph_adapter(payload)
    if provider == "google":
        return await _google_adapter(payload)

    # ── MOCK ──
    print(f"[Calendar mock] Would schedule: {payload['topic']} at {payload['proposed_datetime']}")
    return ToolResult(
        success = True,
        message = f"Meeting scheduled with {payload['customer_name']} (mock)",
        data    = {"event_id": "mock-event-001", "provider": "mock"},
    )


async def _graph_adapter(payload: dict) -> ToolResult:
    import httpx
    from datetime import datetime, timedelta
    token = os.getenv("MS_GRAPH_TOKEN")
    start = payload["proposed_datetime"]
    end   = (
        datetime.fromisoformat(start) + timedelta(minutes=payload["duration_minutes"])
    ).isoformat()

    body = {
        "subject": payload["topic"],
        "start":   {"dateTime": start, "timeZone": "Africa/Cairo"},
        "end":     {"dateTime": end,   "timeZone": "Africa/Cairo"},
        "attendees": [
            {"emailAddress": {"address": payload["customer_email"]}, "type": "required"}
        ],
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(
            "https://graph.microsoft.com/v1.0/me/events",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=body,
        )
        r.raise_for_status()
        event = r.json()
    return ToolResult(
        success = True,
        message = f"Meeting created in Outlook Calendar",
        data    = {"event_id": event.get("id")},
    )


async def _google_adapter(payload: dict) -> ToolResult:
    # Requires: pip install google-api-python-client google-auth
    from googleapiclient.discovery import build  # type: ignore
    from google.oauth2.credentials import Credentials  # type: ignore
    from datetime import datetime, timedelta

    creds = Credentials(token=os.getenv("GOOGLE_CALENDAR_TOKEN"))
    service = build("calendar", "v3", credentials=creds)
    start = payload["proposed_datetime"]
    end   = (
        datetime.fromisoformat(start) + timedelta(minutes=payload["duration_minutes"])
    ).isoformat()

    event = service.events().insert(
        calendarId="primary",
        body={
            "summary": payload["topic"],
            "start":   {"dateTime": start, "timeZone": "Africa/Cairo"},
            "end":     {"dateTime": end,   "timeZone": "Africa/Cairo"},
            "attendees": [{"email": payload["customer_email"]}],
        },
    ).execute()
    return ToolResult(
        success = True,
        message = "Meeting created in Google Calendar",
        data    = {"event_id": event.get("id")},
    )