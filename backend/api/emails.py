from fastapi import APIRouter
from tools.email_tool import execute_email

router = APIRouter()


@router.post("/send")
async def send_email(payload: dict) -> dict:
    customer_id = payload.get("customer_id", "cust_khaled_001")
    rm_id = payload.get("rm_id", "rm_sara_001")
    draft = payload.get("draft") or payload.get("body") or "Hello from RM Copilot"
    to_email = payload.get("to_email") or "esraaaboelkhair8@gmail.com"
    to_name = payload.get("to_name") or payload.get("customer_name") or "Customer"

    result = await execute_email(
        {
            "to_name": to_name,
            "to_email": to_email,
            "subject": payload.get("subject", "Follow-up from RM Copilot"),
            "body": draft,
            "customer_id": customer_id,
            "rm_id": rm_id,
        },
        rm_id,
    )

    return {
        "success": result.success,
        "message": result.message,
        "data": result.data,
        "error": result.error,
    }
