from __future__ import annotations

import hashlib
import json
from datetime import datetime


def point_in_time_join(labels: list[dict], features: list[dict]) -> list[dict]:
    """Pick the most recent feature row at or before each label timestamp."""
    by_entity: dict[str, list[dict]] = {}
    for feature in features:
        by_entity.setdefault(feature["entity_id"], []).append(feature)
    for rows in by_entity.values():
        rows.sort(key=lambda x: x["feature_ts"])

    output = []
    for label in labels:
        candidates = [
            f for f in by_entity.get(label["entity_id"], [])
            if f["feature_ts"] <= label["label_ts"]
        ]
        selected = candidates[-1] if candidates else None
        output.append({**label, **({"features": selected["values"]} if selected else {"features": {}})})
    return output


def dataset_manifest(rows: list[dict], sources: list[str]) -> dict:
    canonical = json.dumps(rows, sort_keys=True, default=str).encode()
    return {
        "dataset_sha256": hashlib.sha256(canonical).hexdigest(),
        "row_count": len(rows),
        "sources": sorted(sources),
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
