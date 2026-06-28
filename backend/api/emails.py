from fastapi import APIRouter

router = APIRouter()


@router.post("/send")
def send_email(payload: dict) -> dict:
    return {"success": True, "message": "Email sent and logged (mock)"}
