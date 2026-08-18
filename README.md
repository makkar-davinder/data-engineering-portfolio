# Data Engineering & AI Platform Portfolio

A set of production-style reference implementations showing how I approach modern data platforms, streaming systems, data quality, and ML/AI data infrastructure.

> **Portfolio note:** All code, schemas, datasets, company names, and metrics in this repository are original or synthetic. The projects demonstrate reusable engineering patterns rather than reproducing proprietary systems from any employer.

## What this repository demonstrates

- Lakehouse architecture with Bronze / Silver / Gold layers
- Kafka-style event streaming and CDC processing patterns
- dbt-style transformation, testing, and analytics engineering
- Data quality, freshness, lineage, and SLA/SLO monitoring
- ML feature / labeling pipelines and training-data preparation
- Cloud-first architecture patterns for AWS, Databricks, Snowflake, Airflow, and Kubernetes
- Engineering leadership thinking: reliability, cost, governance, ownership, and operational tradeoffs

## Projects

| Project | Focus | Technologies / Patterns |
|---|---|---|
| [Lakehouse Platform](projects/lakehouse-platform/) | Governed Bronze/Silver/Gold platform | Python, Delta-style modeling, CDC, data contracts |
| [Streaming Platform](projects/streaming-platform/) | Real-time event processing | Kafka patterns, idempotency, deduplication, retries |
| [Data Quality & Observability](projects/data-quality-observability/) | Reliability and SLOs | freshness checks, schema validation, quality rules |
| [ML Data Platform](projects/ml-data-platform/) | Training and labeling data | feature preparation, point-in-time joins, dataset manifests |

## Architecture principles

1. **Raw data is immutable.** Keep ingestion simple and replayable.
2. **Contracts at boundaries.** Validate schemas and critical business expectations before downstream use.
3. **Idempotent processing.** Reprocessing should not create duplicate business state.
4. **Observable by default.** Freshness, volume, quality, latency, and failure signals are part of the platform.
5. **Separate storage from serving.** Optimize analytical and operational access paths independently.
6. **Cost is an architecture requirement.** Compute, retention, and data movement are designed intentionally.
7. **Self-service with guardrails.** Teams move quickly within clear ownership and governance boundaries.

## Repository layout

```text
data-engineering-portfolio/
├── README.md
├── docs/
│   └── architecture.md
├── projects/
│   ├── lakehouse-platform/
│   ├── streaming-platform/
│   ├── data-quality-observability/
│   └── ml-data-platform/
├── src/common/
├── tests/
├── requirements.txt
└── .gitignore
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

## About me

I build and lead data engineering organizations focused on reliable data platforms, real-time systems, analytics, and AI/ML infrastructure. My work has included platform modernization, streaming architecture, data governance, observability, cloud cost optimization, and building engineering teams that can operate these systems at scale.
