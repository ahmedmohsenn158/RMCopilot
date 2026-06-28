import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

LOG_PATH = Path(__file__).parent / "audit_log.jsonl"


def log_ai_suggestion(
    rm_id: str,
    customer_id: str | None,
    agent: str,
    suggestion: str,
    model: str,
    confidence: float | None = None,
) -> None:
    _write(
        {
            "log_id": str(uuid.uuid4()),
            "type": "ai_suggestion",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "rm_id": rm_id,
            "customer_id": customer_id,
            "agent": agent,
            "model": model,
            "suggestion_preview": suggestion[:200],
            "confidence": confidence,
        }
    )


def log_human_action(rm_id: str, customer_id: str, action: str, context: str) -> None:
    _write(
        {
            "log_id": str(uuid.uuid4()),
            "type": "human_action",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "rm_id": rm_id,
            "customer_id": customer_id,
            "action": action,
            "context": context,
        }
    )


def _write(entry: dict) -> None:
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
