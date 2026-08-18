# Streaming Platform

A compact example of the processing semantics I expect from a production event consumer: validation, idempotency, deduplication, dead-letter handling, and measurable processing outcomes.

The implementation is intentionally broker-independent so the reliability logic is easy to test. In production this pattern can sit behind Kafka/MSK, Kinesis, Pub/Sub, or another durable event bus.
