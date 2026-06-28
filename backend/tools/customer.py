import os
import json
from pathlib import Path
from .base import ProposedAction, ToolResult

DATA_PATH = Path(__file__).parents[2] / "data" / "customers.json"


def search_customer(
    query: str,
    rm_id: str,
) -> ProposedAction:
    """
    Customer search is a read-only tool — still wrapped as ProposedAction
    so the orchestrator handles it uniformly, but no approval needed.
    """
    return ProposedAction(
        tool="search_customer",
        label="Search Customer",
        summary=f"Search for customer: {query}",
        payload={"query": query, "rm_id": rm_id},
    )


async def execute_search(payload: dict, rm_id: str) -> ToolResult:
    """Read-only — no audit log entry needed."""
    try:
        results = await _adapter(payload["query"], payload["rm_id"])
        return ToolResult(
            success = True,
            message = f"Found {len(results)} customer(s)",
            data    = {"customers": results},
        )
    except Exception as exc:
        return ToolResult(success=False, message="Customer search failed", error=str(exc))


async def _adapter(query: str, rm_id: str) -> list[dict]:
    """
    Replace with your core banking API call.

    REST API example:
        import httpx
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{os.getenv('CORE_BANKING_URL')}/customers",
                params={"q": query, "rm_id": rm_id},
                headers={"Authorization": f"Bearer {os.getenv('CORE_BANKING_TOKEN')}"},
            )
            return r.json()["results"]

    Database example (SQLAlchemy):
        from db import SessionLocal, Customer
        with SessionLocal() as session:
            return session.query(Customer).filter(
                Customer.rm_id == rm_id,
                Customer.name.ilike(f"%{query}%")
            ).all()
    """
    provider = os.getenv("CUSTOMER_DATA_PROVIDER", "json").lower()

    if provider == "api":
        return await _api_adapter(query, rm_id)

    # ── JSON fallback ──
    if not DATA_PATH.exists():
        return []
    with open(DATA_PATH) as f:
        customers = json.load(f)

    q = query.lower()
    return [
        c for c in customers
        if c.get("rm_id") == rm_id and (
            q in c.get("name", "").lower() or
            q in c.get("segment", "").lower() or
            q in c.get("customer_id", "").lower()
        )
    ]


async def _api_adapter(query: str, rm_id: str) -> list[dict]:
    import httpx
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{os.getenv('CORE_BANKING_URL')}/customers",
            params={"q": query, "rm_id": rm_id},
            headers={"Authorization": f"Bearer {os.getenv('CORE_BANKING_TOKEN')}"},
            timeout=5.0,
        )
        r.raise_for_status()
        return r.json().get("results", [])