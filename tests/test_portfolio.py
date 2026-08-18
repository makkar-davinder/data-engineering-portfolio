import importlib.util
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).parents[1]


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_lakehouse_deduplicates_latest_order_event():
    p = load("projects/lakehouse-platform/pipeline.py", "lakehouse")
    events = [
        p.OrderEvent("1", "o1", "c1", 10, "created", "2026-01-01T00:00:00Z", 1),
        p.OrderEvent("2", "o1", "c1", 10, "paid", "2026-01-01T00:01:00Z", 2),
    ]
    silver = p.silver(p.bronze(events))
    assert len(silver) == 1
    assert silver[0]["status"] == "paid"


def test_consumer_is_idempotent():
    m = load("projects/streaming-platform/consumer.py", "streaming")
    seen = []
    c = m.IdempotentConsumer(lambda e: seen.append(e.key))
    event = m.Event("e1", "device-1", {"value": 1})
    assert c.consume(event) == "processed"
    assert c.consume(event) == "duplicate"
    assert seen == ["device-1"]


def test_freshness_check():
    q = load("projects/data-quality-observability/checks.py", "quality")
    now = datetime.now(timezone.utc)
    assert q.freshness_check(now - timedelta(minutes=4), 5, now)
    assert not q.freshness_check(now - timedelta(minutes=6), 5, now)


def test_point_in_time_join_avoids_future_feature():
    m = load("projects/ml-data-platform/training_data.py", "ml")
    labels = [{"entity_id": "x", "label_ts": 20, "label": 1}]
    features = [
        {"entity_id": "x", "feature_ts": 10, "values": {"score": 0.2}},
        {"entity_id": "x", "feature_ts": 30, "values": {"score": 0.9}},
    ]
    result = m.point_in_time_join(labels, features)
    assert result[0]["features"]["score"] == 0.2
