from __future__ import annotations


def require_keys(record: dict, keys: set[str]) -> None:
    missing = keys - record.keys()
    if missing:
        raise ValueError(f"missing required keys: {sorted(missing)}")
