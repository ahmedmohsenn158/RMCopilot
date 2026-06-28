from fastapi import APIRouter

from backend.infrastructure.redis_client import get_recent_alerts

router = APIRouter()

@router.get("/{customer_id}")
def get_customer_alerts(customer_id: str) -> list[dict]:
    return get_recent_alerts(customer_id)
