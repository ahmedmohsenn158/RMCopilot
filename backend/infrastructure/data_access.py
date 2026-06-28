import json
from functools import lru_cache
from pathlib import Path

PROJECT_ROOT = Path(__file__).parents[2]
DATA_DIR = PROJECT_ROOT / "data"


@lru_cache(maxsize=1)
def load_customers() -> list[dict]:
    return json.loads((DATA_DIR / "customers.json").read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_events() -> list[dict]:
    return json.loads((DATA_DIR / "sample_events.json").read_text(encoding="utf-8"))


def events_for_customer(customer_id: str) -> list[dict]:
    return [event for event in load_events() if event.get("customer_id") == customer_id]
