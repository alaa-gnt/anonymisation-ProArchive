---
name: data-pipeline-design
description: Design a data pipeline that reliably and efficiently moves data from sources to destinations, with appropriate transformations, error handling, monitoring, and SLAs.
---

# data-pipeline-design

## 1. Work skill name
Data Pipeline Design

## 2. Job to be done
Design a data pipeline that reliably and efficiently moves data from sources to destinations, with appropriate transformations, error handling, monitoring, and SLAs.

## 3. Trigger or use case
- Data needs to move from a transactional database to a data warehouse for analytics
- Real-time data (events, logs, metrics) needs to be processed and stored
- An ML model needs a feature pipeline for training and serving features
- Data needs to be synchronized across multiple systems
- An existing pipeline has reliability, latency, or cost issues

## 4. Required inputs
- Data sources: databases, APIs, event streams, file uploads, third-party services
- Data destinations: data warehouse, data lake, feature store, real-time dashboard
- Data transformation requirements: what fields to extract, clean, join, aggregate
- SLAs: freshness (how old can the data be?), latency (how fast must it arrive?), completeness
- Data volume and growth rate
- Compliance/security: PII handling, GDPR, data retention

## 5. Step-by-step workflow

### Step 1: Understand the data sources and destinations
- Catalog all data sources: schemas, access methods, frequency, volume (FDE Ch.3)
- Catalog all destinations: schemas, access methods, freshness requirements
- Identify the data flow: source → ingestion → transformation → storage → consumption (FDE Ch.1)
- Identify which data is needed and which is optional

### Step 2: Choose between batch and stream processing (FDE Ch.3, DDIA Ch.10-11)
- Use batch when: freshness SLA is > 1 hour, data volume is very large, complex transformations are needed, late-arriving data is acceptable
- Use stream when: freshness SLA is < 1 minute, real-time decisions are needed, event-based processing is required
- Use lambda/kappa architecture when: both batch and stream are needed (batch for accuracy, stream for low latency)
- Often the right answer is: start with batch, add stream when the need is proven

### Step 3: Design the ingestion layer
- For databases: use change data capture (CDC) or periodic extraction (FDE Ch.3, DDIA Ch.11)
- For APIs: use scheduled pulls or webhooks
- For events: use event streaming platforms (Kafka, Kinesis, Pub/Sub) (DDIA Ch.11)
- For files: use scheduled file transfers or event-triggered ingestion
- Plan for schema changes in source systems (DDIA Ch.4)

### Step 4: Design the transformation layer
- Define the transformations needed: cleansing, deduplication, joining, aggregation, enrichment (FDE Ch.3)
- Choose transformation tools: SQL (dbt), Python (Spark, Beam), or orchestrated tasks (Airflow, Dagster)
- Plan for data quality checks: null checks, type checks, range checks, uniqueness checks
- Plan for error handling: dead-letter queues for failed records, retry logic, alerting

### Step 5: Design the storage layer
- Choose the storage format: Parquet (columnar, analytics), Avro (row-oriented, streaming), ORC (Hive-optimized) (DDIA Ch.3, FDE Ch.5)
- Partition strategy: by date, by source, by geography (DDIA Ch.6)
- Compression strategy: snappy (speed) vs. gzip (compression ratio) vs. zstd (balanced)
- Data lifecycle: retention policy, archival, deletion

### Step 6: Design the orchestration and scheduling
- Define the DAG of tasks: order, dependencies, parallelism (FDE Ch.3)
- Define retry logic: number of retries, backoff interval, max duration
- Define alerting: task failure, data quality failure, SLA breach
- Define test strategy: data quality tests run after each pipeline run

### Step 7: Define monitoring and SLAs
- Freshness SLA: how up-to-date must the data be?
- Completeness SLA: what percentage of source data must arrive?
- Latency SLA: what is the maximum time from source to destination?
- Monitor: task success/failure, data volume, latency, data quality metrics
- Alert on: SLA breaches, task failures, data quality violations

## 6. Output deliverable
A data pipeline design document covering: source/destination catalog, ingestion design, transformation design, storage design, orchestration DAG, SLAs, monitoring plan, and error handling strategy.

## 7. Quality checklist
- [ ] All data sources and destinations are cataloged
- [ ] Batch vs. stream decision is justified by freshness requirements
- [ ] Schema changes in source systems are handled
- [ ] Transformations account for data quality (nulls, dedup, validation)
- [ ] Error handling includes dead-letter queues and retry logic
- [ ] Storage format and partitioning match query patterns
- [ ] Orchestration DAG is defined with dependencies
- [ ] SLAs are defined (freshness, completeness, latency)
- [ ] Monitoring covers tasks, data quality, and SLAs
- [ ] Compliance/PII requirements are addressed

## 8. Common failure modes
- Not planning for schema changes (pipeline breaks when a source adds a column) (DDIA Ch.4)
- Choosing stream processing for batch workloads (unnecessary complexity) (DDIA Ch.11)
- Not handling late-arriving data (batch pipeline misses records) (DDIA Ch.10)
- No dead-letter queue for failed records (data silently lost)
- Not monitoring data volume trends (data grows 10x and pipeline silently slows down)
- Under-partitioning (huge files that are hard to process) or over-partitioning (millions of tiny files) (DDIA Ch.6)
- Not testing data quality (pipeline runs successfully but produces wrong data) (FDE Ch.5)
- Not handling PII/security requirements from the start (retrofit is expensive) (FDE Ch.2)
- Building the pipeline before understanding the consumption patterns (wrong schema for analytics) (FDE Ch.5)
- Not planning for full re-processing when logic changes (DDIA Ch.10, Ch.11)

## 9. Dependencies on framework skills
- Data Modeling (for schema design)
- Systems Thinking (for feedback loops and delay analysis)
- ML System Design (if pipeline feeds ML models)

## 10. Source books used
- Primary: Fundamentals of Data Engineering (Reis & Housley)
- Support: Designing Data-Intensive Applications (Kleppmann), Designing Machine Learning Systems (Huyen), Machine Learning Design Patterns (Lakshmanan et al.)

## 11. Example of a good final output structure
```
# Data Pipeline: Order Analytics Pipeline

## Sources
- PostgreSQL (orders DB) — CDC via Debezium
- Payment API — hourly pull
- Mobile app events — Kinesis stream

## Destination
- Snowflake (data warehouse) — order analytics dashboard

## Ingestion
- CDC from Postgres → Kafka (real-time)
- API pull → Airflow DAG (hourly)
- Kinesis → Firehose → S3 (near-real-time)

## Transformations (dbt)
- stg_orders: type casting, null handling
- stg_payments: dedup by payment_id
- fct_orders: join orders + payments, calculate totals
- dim_customers: SCD Type 2 for address changes

## Storage
- S3 as data lake (Parquet, partitioned by date)
- Snowflake as data warehouse (transformed models)

## Orchestration
- Airflow DAG: ingestion → staging → transformation → load
- Retry: 3 times, 5 min exponential backoff
- Alert: Slack on failure, PagerDuty if 2+ consecutive failures

## SLAs
- Freshness: < 1 hour for order data
- Completeness: > 99.9% of orders arrive within SLA
- Latency: < 30 min from order placement to dashboard
```
