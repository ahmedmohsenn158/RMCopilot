import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv()
load_dotenv(PROJECT_ROOT / ".env", override=True)

DEFAULT_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant").strip()


async def chat_completion(
    system: str,
    user: str,
    *,
    model: str | None = None,
    temperature: float = 0.3,
) -> str:
    api_key = _env_value("GROQ_API_KEY")
    selected_model = model or DEFAULT_MODEL

    if not api_key:
        print("[Groq] GROQ_API_KEY is missing; using demo response.")
        return _offline_reply(system, user)

    from groq import AsyncGroq

    client = AsyncGroq(api_key=api_key)
    try:
        response = await client.chat.completions.create(
            model=selected_model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return response.choices[0].message.content or ""
    except Exception as exc:
        if _is_auth_error(exc):
            print(
                "[Groq] API key was rejected by Groq. Update GROQ_API_KEY in "
                f"{PROJECT_ROOT / '.env'} and restart the backend."
            )
        else:
            print(f"[Groq] Falling back to demo response: {exc}")
        return _offline_reply(system, user)


def model_name() -> str:
    return DEFAULT_MODEL


def _env_value(name: str) -> str:
    return os.getenv(name, "").strip().strip("\"'")


def _is_auth_error(exc: Exception) -> bool:
    status_code = getattr(exc, "status_code", None)
    message = str(exc).lower()
    return status_code in {401, 403} or "invalid_api_key" in message or "invalid api key" in message


def _offline_reply(system: str, user: str) -> str:
    text = f"{system}\n{user}".lower()
    if "fx" in text or "eligible" in text or "product" in text:
        return (
            "Khaled is a strong candidate for an FX Forward Contract because his account shows repeated USD activity "
            "and import exposure. A practical pitch is: given your recent USD flows, we can lock a future exchange "
            "rate now so a 2% to 3% currency move does not erode your margin."
        )
    if "breach" in text or "limit" in text:
        return (
            "The most urgent issue is the credit-limit breach. Ask the customer what caused the excess, confirm whether "
            "incoming funds are expected, notify Credit, and log the explanation in CRM."
        )
    if "draft" in text or "email" in text or "crm" in text:
        return (
            "Dear Khaled,\n\nThank you for speaking with me today. I will coordinate the trade finance review and send "
            "the FX hedging information we discussed. I will follow up with the next steps once Credit confirms the "
            "available options.\n\n[Review before sending - do not send without RM approval]"
        )
    if "suspicious" in text or "anomaly" in text:
        return (
            "This activity is materially outside the customer's usual pattern and should be clarified before any further "
            "action. Ask the customer to confirm the purpose, counterparty, and whether they expected this transfer."
        )
    return (
        "I can help with customer context, product guidance, policy steps, alerts, and follow-up drafts. For this case, "
        "check the customer's open alerts first, then record the next action in CRM."
    )
