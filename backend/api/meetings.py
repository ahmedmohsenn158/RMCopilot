from fastapi import APIRouter

from infrastructure.data_access import load_events
from mocks.customer_mock import get_customer

router = APIRouter()


@router.get("/")
def list_meetings(rm_id: str = "rm_sara_001") -> list[dict]:
    meetings = []
    for event in load_events():
        if event.get("event_type") != "meeting_scheduled":
            continue
        customer = get_customer(event["customer_id"])
        if not customer or customer.get("rm_id") != rm_id:
            continue
        meetings.append(
            {
                "id": event["event_id"],
                "time": event.get("meeting_time", "9:00 AM"),
                "name": customer["name"],
                "initials": customer.get("initials", ""),
                "topic": event.get("topic", "Customer meeting"),
                "segment": f"{customer['segment']} {customer['tier']}",
                "color": "accent" if customer["tier"] == "Gold" else "success",
                "status": "urgent" if customer["customer_id"] == "cust_khaled_001" else "normal",
            }
        )
    return meetings


@router.post("/brief")
def prepare_meeting_brief(payload: dict) -> dict:
    name = payload.get("customerName", "customer")
    topic = payload.get("topic", "meeting")
    return {"success": True, "brief": f"Meeting brief generated for {name} - {topic}"}
