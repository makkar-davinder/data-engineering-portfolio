"""Small, dependency-light Bronze -> Silver -> Gold reference pipeline."""
from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Iterable


@dataclass(frozen=True)
class OrderEvent:
    event_id: str
    order_id: str
    customer_id: str
    amount: float
    status: str
    event_ts: str
    source_offset: int

    def validate(self) -> None:
        if not self.event_id or not self.order_id or not self.customer_id:
            raise ValueError("event_id, order_id and customer_id are required")
        if self.amount < 0:
            raise ValueError("amount cannot be negative")
        if self.status not in {"created", "paid", "shipped", "cancelled"}:
            raise ValueError(f"unsupported status: {self.status}")
        datetime.fromisoformat(self.event_ts.replace("Z", "+00:00"))


def bronze(events: Iterable[OrderEvent]) -> list[dict]:
    """Preserve raw source values plus ingestion metadata."""
    ingested_at = datetime.now(timezone.utc).isoformat()
    return [{**asdict(e), "ingested_at": ingested_at} for e in events]


def silver(bronze_rows: Iterable[dict]) -> list[dict]:
    """Validate and keep the latest CDC event for each order."""
    latest: dict[str, dict] = {}
    for row in bronze_rows:
        event = OrderEvent(**{k: row[k] for k in OrderEvent.__dataclass_fields__})
        event.validate()
        current = latest.get(event.order_id)
        if current is None or event.source_offset > current["source_offset"]:
            latest[event.order_id] = row
    return list(latest.values())


def gold_customer_summary(silver_rows: Iterable[dict]) -> list[dict]:
    """Create a simple customer-level analytical model."""
    agg = defaultdict(lambda: {"orders": 0, "revenue": 0.0})
    for row in silver_rows:
        if row["status"] == "cancelled":
            continue
        agg[row["customer_id"]]["orders"] += 1
        agg[row["customer_id"]]["revenue"] += row["amount"]
    return [
        {"customer_id": cid, "orders": x["orders"], "revenue": round(x["revenue"], 2)}
        for cid, x in sorted(agg.items())
    ]


if __name__ == "__main__":
    sample = [
        OrderEvent("e1", "o1", "c1", 49.99, "created", "2026-01-01T10:00:00Z", 1),
        OrderEvent("e2", "o1", "c1", 49.99, "paid", "2026-01-01T10:01:00Z", 2),
        OrderEvent("e3", "o2", "c1", 25.00, "paid", "2026-01-01T10:02:00Z", 3),
        OrderEvent("e4", "o3", "c2", 80.00, "cancelled", "2026-01-01T10:03:00Z", 4),
    ]
    b = bronze(sample)
    s = silver(b)
    print(gold_customer_summary(s))
