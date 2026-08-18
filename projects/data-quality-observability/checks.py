from __future__ import annotations

from datetime import datetime, timedelta, timezone
from statistics import mean


def freshness_check(latest_event_ts: datetime, max_age_minutes: int, now: datetime | None = None) -> bool:
    now = now or datetime.now(timezone.utc)
    return now - latest_event_ts <= timedelta(minutes=max_age_minutes)


def uniqueness_check(rows: list[dict], key: str) -> bool:
    values = [r.get(key) for r in rows]
    return len(values) == len(set(values))


def required_fields_check(rows: list[dict], fields: list[str]) -> bool:
    return all(all(row.get(field) is not None for field in fields) for row in rows)


def accepted_values_check(rows: list[dict], field: str, accepted: set) -> bool:
    return all(row.get(field) in accepted for row in rows)


def volume_anomaly(current_count: int, historical_counts: list[int], tolerance: float = 0.30) -> bool:
    if not historical_counts:
        return False
    baseline = mean(historical_counts)
    if baseline == 0:
        return current_count != 0
    return abs(current_count - baseline) / baseline > tolerance
