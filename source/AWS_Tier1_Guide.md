# AWS Tier-1 Mastery Guide: Cloud & Data Engineering

---

## 1. Core AWS Services (20+)

### Compute & Serverless
- **EC2 (Elastic Compute Cloud):** Resizable compute capacity; instances (On-demand, Spot, Reserved).
- **Lambda:** Event-driven, serverless compute; handles scaling automatically.
- **EKS (Elastic Kubernetes Service):** Managed Kubernetes for container orchestration.
- **ECS (Elastic Container Service):** Fully managed container orchestration.
- **Fargate:** Serverless compute for containers (no managing EC2s).
- **Batch:** Managed batch processing for Docker-based workloads.
- **Step Functions:** Serverless visual workflow orchestration (State Machines).

### Storage & Content Delivery
- **S3 (Simple Storage Service):** Object storage; 99.999999999% (11 9's) durability.
- **EFS (Elastic File System):** Managed NFS for EC2/Lambda.
- **EBS (Elastic Block Store):** Network-attached block storage for EC2.
- **CloudFront:** Global Content Delivery Network (CDN) using Edge Locations.

### Databases & Cache
- **RDS (Relational Database Service):** Managed SQL (Postgres, MySQL, Oracle, etc.).
- **Aurora:** AWS-native relational DB (Postgres/MySQL compatible) with 3x-5x performance.
- **DynamoDB:** NoSQL key-value/document DB with millisecond latency.
- **ElastiCache:** Managed Redis/Memcached for in-memory caching.
- **Redshift:** Managed Data Warehouse for OLAP workloads.

### Data Analytics & Integration
- **Glue:** Serverless ETL (Extract, Transform, Load) with Cataloging.
- **Athena:** Serverless SQL queries directly on S3 (Presto-based).
- **EMR (Elastic MapReduce):** Managed Hadoop, Spark, Hive, Presto.
- **Kinesis Data Streams:** High-throughput streaming data collection.
- **Kinesis Firehose:** Load streaming data into S3/Redshift/Elasticsearch.
- **MSK (Managed Streaming for Kafka):** Fully managed Apache Kafka.
- **SQS (Simple Queue Service):** Fully managed message queuing.
- **SNS (Simple Notification Service):** Pub/Sub messaging service.
- **EventBridge:** Serverless event bus (successor to CloudWatch Events).

### Security & Governance
- **IAM (Identity and Access Management):** Roles, Policies, Users, Groups.
- **VPC (Virtual Private Cloud):** Isolated network (Subnets, Route Tables, IGW).
- **CloudWatch:** Monitoring, Logs, Metrics, Alarms.
- **CloudTrail:** API activity auditing.

---

## 2. Real-World Pipelines

### A. Batch Processing Pipeline (Daily Aggregations)
**Flow:** `S3 (Landing) → Glue ETL (Spark) → S3 (Curated) → Redshift Spectrum / Athena`
- **Use Case:** Daily sales reporting or user behavior analysis.
- **Description:** Data arrives in CSV/JSON in S3. Glue Crawler updates the Data Catalog. A Glue Spark job cleans, joins, and converts data to Parquet (partitioned by date). Final data is queried via Redshift for BI dashboards.

### B. Streaming Pipeline (Real-Time Analytics)
**Flow:** `App Logs → Kinesis Data Streams → Lambda (Transformation) → DynamoDB (Live Dashboard) & S3 (Long-term)`
- **Use Case:** Real-time fraud detection or live leaderboard.
- **Description:** Producers push logs to Kinesis. A Lambda function consumes shards, calculates metrics (e.g., rolling averages), and updates a DynamoDB table for low-latency UI access. Firehose simultaneously archives raw logs to S3.

### C. CDC (Change Data Capture) Pipeline
**Flow:** `RDS (MySQL) → DMS (Database Migration Service) → S3 → Glue/Athena`
- **Use Case:** Syncing production DB to a Data Lake without impacting performance.
- **Description:** DMS reads binlogs from RDS and streams changes as Parquet files to S3. Athena provides a SQL layer for analysts to query the "near real-time" replica of the database.

---

## 3. Internal Deep Dives

### S3: Request Routing & Prefix Partitioning
- **Architecture:** S3 is not a filesystem; it’s an object store. Behind the scenes, it uses an index managed by "partitions."
- **Partition Limits:** A single S3 prefix (folder) can handle:
  - **3,500 PUT/COPY/POST/DELETE** requests per second.
  - **5,500 GET/HEAD** requests per second.
- **Scale Out:** If you hit these limits, S3 automatically splits the prefix into sub-partitions. 
- **Interview Tip:** To maximize performance for massive parallel loads, use a high-cardinality prefix strategy (e.g., `/data/customer_id/date/` instead of just `/data/date/`).

### Lambda: Cold Starts & Concurrency
- **Cold Start:** The latency incurred when AWS initializes a new execution environment (downloading code, starting runtime).
- **Concurrency Types:**
  - **Reserved Concurrency:** Guaranteed capacity for a specific function (also acts as a limit).
  - **Provisioned Concurrency:** Keeps environments "warm" to eliminate cold starts (costs extra).
- **Math:** Concurrency = `Average Requests Per Second * Average Execution Duration (seconds)`.

### Kinesis: Shard Math (VERY Important)
- **Shard Capacity:**
  - **Input (Write):** 1 MB/sec or 1,000 records/sec per shard.
  - **Output (Read):** 2 MB/sec per shard.
- **Calculation:** If your data producer sends 10MB/s, you need at least `10 / 1 = 10` shards. 
- **Scaling:** Resharding (Splitting or Merging shards) allows you to scale up or down based on throughput.

---

## 4. Interview Q&A

**Q: How do you choose between SQS and Kinesis?**
- **A:** Choose **SQS** for decoupled task processing where each message is processed independently (worker-pattern). Choose **Kinesis** for data streaming where the order of records matters and multiple consumers need to read the same stream (replayability).

**Q: What is the difference between Redshift and Athena?**
- **A:** **Redshift** is a persistent, high-performance Data Warehouse (OLAP) with its own storage and compute. **Athena** is a serverless query engine that reads directly from S3. Use Redshift for complex, frequent BI queries; use Athena for ad-hoc exploration of S3 data.

**Q: How do you handle a Lambda Cold Start?**
- **A:** Use **Provisioned Concurrency** for critical paths, minimize package size (remove unused dependencies), and use languages with faster startup times (Go/Node.js vs. Java).

---

## 5. Resume-Ready Explanations

- **Data Pipeline Optimization:** "Architected a multi-stage ETL pipeline using **AWS Glue (Spark)** and **S3**, reducing processing time by 40% through efficient **prefix partitioning** and **Parquet conversion**."
- **Real-Time Streaming:** "Implemented a real-time monitoring system using **Kinesis Data Streams** and **AWS Lambda**, processing over 500k events/minute with sub-second latency for fraud detection."
- **Infrastructure as Code:** "Deployed a highly available **EKS cluster** with **VPC** isolation and **IAM** fine-grained access, supporting 50+ microservices with automated scaling."
- **Cost Savings:** "Reduced AWS monthly spend by 25% by migrating dev workloads to **Fargate** and implementing **Lambda** Provisioned Concurrency only during peak hours."

---

## 6. Architecture Diagram Concepts (Visual Flow)

1. **Batch Flow:**
   `App Service` -> `S3` -> `EventBridge` -> `Lambda` -> `Glue Trigger` -> `Glue Job` -> `S3 (Curated)` -> `Redshift`.
2. **Streaming Flow:**
   `IoT Devices` -> `Kinesis` -> `Lambda (Schema Check)` -> `Firehose` -> `S3` -> `Athena`.

---
*Generated for Tier-1 Professional Development*
