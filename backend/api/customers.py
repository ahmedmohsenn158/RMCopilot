from fastapi import APIRouter, HTTPException

from mocks.customer_mock import get_customer, search_customers, to_active_customer, to_customer_search_item

router = APIRouter()


@router.get("/")
def list_customers(rm_id: str = "rm_sara_001", query: str = "") -> list[dict]:
    return [to_customer_search_item(c) for c in search_customers(rm_id, query)]


@router.get("/{customer_id}")
def get_customer_profile(customer_id: str) -> dict:
    customer = get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return to_active_customer(customer)
