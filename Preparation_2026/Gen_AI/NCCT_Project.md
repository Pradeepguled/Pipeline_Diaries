1️⃣ Start with the problem (business first)

“I work on NCCT, a healthcare cost transparency project for Blue Cross Blue Shield Association.
The goal is to analyze insurance claims and understand how much hospitals and doctors usually charge for treatments.”

2️⃣ High-level tech overview

“It’s a batch data engineering pipeline built on AWS and Snowflake, using Spark for large-scale data processing.”

3️⃣ Walk through the pipeline (end to end)

“We first validate incoming files using AWS Lambda.
Then we ingest data into S3 and Snowflake using AWS Glue and Snowpipe.”

“We extract claims data, enrich it with provider network information, classify services, and calculate historical volume and rate metrics.”

“Finally, we generate submission tables that are delivered to BCBSA.”

4️⃣ Data modeling & correctness

“In Snowflake, data is modeled using a star schema.
We use SCD Type-2 and separate history tables to maintain historical accuracy.”

  ┌────────────────────────────┐
              │   Upstream Sources          │
              │ (Claims, Provider, Network) │
              └─────────────┬──────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │  S3 Landing Zone  │
                  │  (Incoming Files)│
                  └─────────┬────────┘
                            │ S3 Event
                            ▼
                  ┌──────────────────┐
                  │ AWS Lambda        │
                  │ File Validation  │
                  │ - schema check   │
                  │ - duplicates     │
                  │ - size/format    │
                  └───────┬──────────┘
            Reject/Alert ▲ │ Pass
                          ▼
              ┌────────────────────────┐
              │   S3 Bronze (Raw)       │
              │  Immutable, partitioned│
              │  by date/source        │
              └─────────┬──────────────┘
                        │
                        ▼
              ┌────────────────────────┐
              │ AWS Glue / Spark ETL    │
              │ - cleansing             │
              │ - enrichment            │
              │ - joins & rules         │
              │ - deduplication         │
              └─────────┬──────────────┘
                        │
                        ▼
              ┌────────────────────────┐
              │  S3 Curated (Parquet)   │
              │  Standardized datasets  │
              └─────────┬──────────────┘
                        │
                        ▼
              ┌────────────────────────┐
              │ Snowpipe (Auto Load)    │
              └─────────┬──────────────┘
                        ▼
              ┌────────────────────────┐
              │ Snowflake Staging       │
              │  (stg_claims, etc.)     │
              └─────────┬──────────────┘
                        ▼
              ┌────────────────────────┐
              │ Snowflake Core Model    │
              │ Star Schema             │
              │ - Fact Claims           │
              │ - Dim Provider (SCD2)   │
              │ - Dim Service           │
              │ - Dim Network (SCD2)    │
              └─────────┬──────────────┘
                        ▼
              ┌────────────────────────┐
              │ Aggregations & Metrics  │
              │ - Volume               │
              │ - Rate metrics         │
              │ - Historical accuracy  │
              └─────────┬──────────────┘
                        ▼
              ┌────────────────────────┐
              │ Submission Tables       │
              │ (BCBSA format)          │
              └─────────┬──────────────┘
                        ▼
              ┌────────────────────────┐
              │ S3 Outbound / Delivery  │
              │ to BCBSA                │
              └────────────────────────┘

---

## NCCT Architecture – Visual Reference

![Image](https://d2908q01vomqb2.cloudfront.net/b6692ea5df920cad691c20319a6fffd7a4a766b8/2021/03/30/bdb1348-simplify-snowflake-databrew-1.jpg)

![Image](https://d2908q01vomqb2.cloudfront.net/b6692ea5df920cad691c20319a6fffd7a4a766b8/2024/08/05/BDB-4096-arch-diagram-752x630.jpg)

![Image](https://media.thoughtspot.com/35707/1690420374-snowflakeschema.png)

![Image](https://www.exasol.com/app/uploads/2025/06/content-hub-post-data-warehouse-concepts-patterns-1280x853.jpg)

*(These are representative architectures — your explanation + flow is what matters in interviews.)*

---

## NCCT End-to-End Architecture (Interview-ready diagram)

```
              ┌────────────────────────────┐
              │   Upstream Sources          │
              │ (Claims, Provider, Network) │
              └─────────────┬──────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │  S3 Landing Zone  │
                  │  (Incoming Files)│
                  └─────────┬────────┘
                            │ S3 Event
                            ▼
                  ┌──────────────────┐
                  │ AWS Lambda        │
                  │ File Validation  │
                  │ - schema check   │
                  │ - duplicates     │
                  │ - size/format    │
                  └───────┬──────────┘
            Reject/Alert ▲ │ Pass
                          ▼
              ┌────────────────────────┐
              │   S3 Bronze (Raw)       │
              │  Immutable, partitioned│
              │  by date/source        │
              └─────────┬──────────────┘
                        │
                        ▼
              ┌────────────────────────┐
              │ AWS Glue / Spark ETL    │
              │ - cleansing             │
              │ - enrichment            │
              │ - joins & rules         │
              │ - deduplication         │
              └─────────┬──────────────┘
                        │
                        ▼
              ┌────────────────────────┐
              │  S3 Curated (Parquet)   │
              │  Standardized datasets  │
              └─────────┬──────────────┘
                        │
                        ▼
              ┌────────────────────────┐
              │ Snowpipe (Auto Load)    │
              └─────────┬──────────────┘
                        ▼
              ┌────────────────────────┐
              │ Snowflake Staging       │
              │  (stg_claims, etc.)     │
              └─────────┬──────────────┘
                        ▼
              ┌────────────────────────┐
              │ Snowflake Core Model    │
              │ Star Schema             │
              │ - Fact Claims           │
              │ - Dim Provider (SCD2)   │
              │ - Dim Service           │
              │ - Dim Network (SCD2)    │
              └─────────┬──────────────┘
                        ▼
              ┌────────────────────────┐
              │ Aggregations & Metrics  │
              │ - Volume               │
              │ - Rate metrics         │
              │ - Historical accuracy  │
              └─────────┬──────────────┘
                        ▼
              ┌────────────────────────┐
              │ Submission Tables       │
              │ (BCBSA format)          │
              └─────────┬──────────────┘
                        ▼
              ┌────────────────────────┐
              │ S3 Outbound / Delivery  │
              │ to BCBSA                │
              └────────────────────────┘
```

---

## How to **explain this diagram in 30 seconds** (important 🔥)

> “Files land in S3 and are validated by Lambda so bad data never enters the system.
> Valid data is stored immutably in S3 raw. Glue Spark jobs enrich and standardize claims data and write curated Parquet files.
> Snowpipe loads this into Snowflake staging, where we build star-schema models using SCD Type-2 to maintain historical correctness.
> We compute volume and rate metrics and finally generate submission tables that are delivered to BCBSA.”

---

## If interviewer asks **WHY this design**

* **Lambda upfront** → cheap, fast failure prevention
* **S3 Bronze** → replay, audit, compliance
* **Spark for heavy joins** → scalable for large claims volume
* **Snowflake for modeling** → analytics, SCD2, aggregation
* **Star schema** → performance + reporting correctness

---
