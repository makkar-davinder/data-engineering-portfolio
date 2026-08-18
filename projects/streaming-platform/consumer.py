from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Event:
    event_id: str
    key: str
    payload: dict


class IdempotentConsumer:
    def __init__(self, handler: Callable[[Event], None]):
        self.handler = handler
        self.processed: set[str] = set()
        self.dead_letter: list[tuple[Event, str]] = []
        self.metrics = {"processed": 0, "duplicates": 0, "failed": 0}

    def consume(self, event: Event) -> str:
        if not event.event_id or not event.key:
            self.metrics["failed"] += 1
            self.dead_letter.append((event, "missing event_id or key"))
            return "failed"

        if event.event_id in self.processed:
            self.metrics["duplicates"] += 1
            return "duplicate"

        try:
            self.handler(event)
        except Exception as exc:  # production code would classify retryable failures
            self.metrics["failed"] += 1
            self.dead_letter.append((event, str(exc)))
            return "failed"

        self.processed.add(event.event_id)
        self.metrics["processed"] += 1
        return "processed"
