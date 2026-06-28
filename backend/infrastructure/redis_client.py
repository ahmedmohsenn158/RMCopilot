import json
import os
import redis
from backend.infrastructure.data_access import events_for_customer, load_events


def _redis_client():
    try:
        client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"), decode_responses=True)
        client.ping()
        return client
    except Exception:
        return None


def seed_redis_from_file() -> int:
    client = _redis_client()
    events = load_events()
    if client is None:
        return 0

    for event in events:
        client.xadd(f"events:{event['customer_id']}", {"data": json.dumps(event)})
    return len(events)


def get_recent_alerts(customer_id: str, count: int = 10) -> list[dict]:
    client = _redis_client()
    if client is not None:
        try:
            raw = client.xrevrange(f"events:{customer_id}", count=count)
            return [_event_to_alert(json.loads(fields["data"])) for _, fields in raw]
        except Exception:
            pass

    return [_event_to_alert(event) for event in events_for_customer(customer_id)][-count:]


def _event_to_alert(event: dict) -> dict:
    event_type = event.get("event_type")
    if event_type == "credit_limit_breach":
        return {
            "id": event["event_id"],
            "type": "danger",
            "title": "Credit limit breach",
            "body": f"Utilisation hit {event['utilisation_pct']}%. Balance is EGP {event['balance_egp']:,} against limit EGP {event['limit_egp']:,}.",
            "time": "2 min ago",
            "actionLabel": "Draft response script",
            "actionPrompt": "Draft a response script for the credit limit breach on Khaled Al-Sayed",
            "raw": event,
        }
    if event_type == "product_expiry":
        return {
            "id": event["event_id"],
            "type": "warning",
            "title": "Product expiry",
            "body": f"{event['product'].replace('_', ' ').title()} expires in {event['days_remaining']} days.",
            "time": "Today",
            "actionLabel": None,
            "raw": event,
        }
    if event_type == "cross_sell_signal":
        return {
            "id": event["event_id"],
            "type": "info",
            "title": "Cross-sell signal",
            "body": event.get("signal", "Cross-sell opportunity detected."),
            "time": "This week",
            "actionLabel": "Expand pitch",
            "actionPrompt": f"Generate a product pitch for {event.get('recommended_product', 'the recommended product')}",
            "raw": event,
        }
    if event_type == "suspicious_pattern":
        return {
            "id": event["event_id"],
            "type": "danger",
            "title": "Suspicious pattern",
            "body": event.get("pattern", "Suspicious account activity detected."),
            "time": "Recent",
            "actionLabel": "Suggest next step",
            "actionPrompt": "Suggest the next step for this suspicious transaction pattern",
            "raw": event,
        }
    return {
        "id": event["event_id"],
        "type": "info",
        "title": event_type.replace("_", " ").title() if event_type else "Event",
        "body": event.get("action") or event.get("topic") or "Customer event recorded.",
        "time": "Recent",
        "actionLabel": None,
        "raw": event,
    }
