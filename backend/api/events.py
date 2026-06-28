from fastapi import APIRouter

from backend.infrastructure.data_access import load_events

router = APIRouter()


@router.get("/")
def list_events(customer_id: str | None = None) -> list[dict]:
    events = load_events()
    if customer_id:
        return [e for e in events if e.get("customer_id") == customer_id]
    return events
