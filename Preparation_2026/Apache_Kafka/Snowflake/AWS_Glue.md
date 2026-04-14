# 1. What is AWS Glue

Amazon Web Services **Glue** is a **serverless ETL service**.

👉 ETL = Extract → Transform → Load

---

## Simple Idea

```text
Take data → clean/transform → load into target
```

No servers to manage.

---

## Example

```text
S3 (raw data)
   ↓
Glue Job (clean/transform)
   ↓
Snowflake / Redshift
```

---

## Short Interview Answer

> AWS Glue is a serverless ETL service that uses Spark to process and transform data without managing infrastructure.

---

# 2. AWS Glue Architecture

```text
Data Source (S3 / DB)
      ↓
Crawler
      ↓
Data Catalog
      ↓
Glue Job
      ↓
Target (S3 / Snowflake / Redshift)
```

---

# 3. Glue Crawler

## Definition

Automatically detects schema and creates tables.

---

## How it works

```text
Reads data
   ↓
Infers schema
   ↓
Creates table in Data Catalog
```

---

## Example

```text
sales.csv → sales_table (id, amount, date)
```

---

## Short Answer

> A Glue Crawler scans data sources and automatically creates metadata tables.

---

# 4. Glue Data Catalog

## Definition

Central metadata store.

---

## Stores

```text
Tables
Schemas
Partitions
```

---

## Simple Idea

```text
Like a dictionary for your data
```

---

## Short Answer

> Glue Data Catalog stores metadata like table structure and schema.

---

# 5. Glue Job

## Definition

Where actual ETL processing happens.

---

## Flow

```text
Read → Transform → Write
```

---

## Example

```text
Read CSV → clean data → write Parquet
```

---

## Types

```text
Spark Job
Python Shell Job
Streaming Job
```

---

## Short Answer

> Glue Job processes and transforms data using Spark or Python.

---

# 6. DynamicFrame vs DataFrame (Important)

| Feature            | DynamicFrame | DataFrame  |
| ------------------ | ------------ | ---------- |
| Schema             | Flexible     | Fixed      |
| Handles messy data | Yes          | No         |
| Use case           | ETL          | Processing |

---

## Key Point

```text
DynamicFrame = best for semi-structured data
```

---

## Short Answer

> DynamicFrame is a Glue abstraction that handles schema inconsistencies and semi-structured data.

---

# 7. Glue Bookmark (Incremental Load)

## Definition

Tracks processed data and loads only new data.

---

## Flow

```text
First run → process all data
   ↓
Save bookmark
   ↓
Next run → process only new data
```

---

## Example

```text
file1, file2 → first run
file3 → next run processes only file3
```

---

## Short Answer

> Glue Bookmark ensures incremental processing by tracking already processed data.

---

# 8. Glue Triggers

## Definition

Used to start jobs automatically.

---

## Types

```text
On-demand
Scheduled
Event-based
```

---

# 9. Glue Workflow

## Definition

Used to manage multiple jobs with dependencies.

---

## Example

```text
Job1 → Job2 → Job3
```

---

# 10. Glue Partitioning

## Example

```text
s3://data/year=2025/month=03/
```

---

## Benefits

```text
Faster queries
Less data scan
```

---

# 11. Handling Semi-Structured Data

Glue handles JSON, Parquet using **DynamicFrame**.

---

## Features

```text
Handles nested data
Handles missing columns
Schema flexibility
```

---

## Example

```text
JSON → flatten → structured table
```

---

# 12. Schema Evolution

## Definition

Handling changing data structure.

---

## How Glue Handles

```text
DynamicFrame → handles changes
Crawler → updates schema
ResolveChoice → fixes type conflicts
```

---

## Example

```text
Day1 → id, name
Day2 → id, name, age
→ Glue handles automatically
```

---

# 13. Glue Bookmark vs Checkpointing

| Feature  | Glue Bookmark  | Checkpointing      |
| -------- | -------------- | ------------------ |
| Tracks   | Data processed | Execution progress |
| Use case | Batch ETL      | Streaming          |

---

# 14. Glue vs EMR vs Lambda

## Glue vs EMR

| Glue       | EMR           |
| ---------- | ------------- |
| Serverless | Cluster-based |
| Easy       | More control  |

---

## Glue vs Lambda

| Glue         | Lambda      |
| ------------ | ----------- |
| Big data ETL | Small tasks |
| Spark-based  | Event-based |

---

# 15. Glue + Snowflake Pipeline

```text
Source
   ↓
S3
   ↓
Glue Job
   ↓
Snowflake (COPY INTO / Snowpipe)
   ↓
Analytics
```

---

# 16. Key Interview Points

```text
Glue is serverless
Uses Spark internally
Crawler → schema detection
Catalog → metadata
Job → processing
DynamicFrame → flexible data
Bookmark → incremental load
```

---

# 17. Quick Revision Summary

```text
Glue → ETL service
Crawler → finds schema
Catalog → stores metadata
Job → processes data
DynamicFrame → flexible
Bookmark → incremental
Triggers → automation
Workflow → orchestration
```

---

# 🎯 Final Interview Answer

If asked:

**Explain AWS Glue**

> AWS Glue is a serverless ETL service that uses Spark to process data. It includes Crawlers for schema detection, Data Catalog for metadata storage, and Glue Jobs for transformation. It also supports incremental processing using bookmarks.

---

Perfect 👍 — these are **high-impact interview topics**. I’ll keep them **simple + practical + interview-ready**.

---

# 1. Glue Performance Tuning (Very Important)

## Problem

Glue jobs can be:

```text
Slow ❌
Expensive ❌
```

---

## Key Techniques

### 1️⃣ Partitioning (Most Important)

Store data like:

```text
s3://data/year=2025/month=03/
```

👉 Glue reads only required partitions → faster.

---

### 2️⃣ Pushdown Predicate

Filter data early:

```python
dyf = glueContext.create_dynamic_frame.from_catalog(
    database="db",
    table_name="table",
    push_down_predicate="year=2025"
)
```

👉 Avoids reading full dataset.

---

### 3️⃣ Use Correct File Format

```text
CSV → slow ❌
Parquet → fast ✅
```

👉 Columnar formats improve performance.

---

### 4️⃣ Avoid Small Files Problem

```text
1000 small files → slow ❌
Few large files → fast ✅
```

👉 Ideal file size: **100MB–250MB**

---

### 5️⃣ Tune DPU (Compute)

More DPUs → faster job

But:

```text
Too many DPUs → costly ❌
```

---

### 6️⃣ Use Bookmark (Incremental)

```text
Process only new data
```

---

### 7️⃣ Convert to DataFrame (Sometimes)

For heavy operations:

```python
df = dyf.toDF()
```

👉 Spark DataFrame is faster for complex transformations.

---

## Short Interview Answer

> Glue performance can be optimized using partitioning, pushdown predicates, efficient file formats like Parquet, avoiding small files, tuning DPUs, and using bookmarks for incremental processing.

---

# 2. Handling CDC (Updates & Deletes)

## Problem

Glue Bookmark only handles:

```text
New data (append) ✅
Updates ❌
Deletes ❌
```

---

## Solution Options

---

### 1️⃣ Full Load + Overwrite

```text
Reload entire table
```

❌ Not efficient

---

### 2️⃣ Use Timestamp Column

```text
last_updated column
```

Process only changed records.

---

### 3️⃣ Use MERGE (Best Practice)

After loading into target (like Snowflake):

```sql
MERGE INTO target t
USING source s
ON t.id = s.id
WHEN MATCHED THEN UPDATE
WHEN NOT MATCHED THEN INSERT;
```

---

### 4️⃣ SCD Type 2 (Very Important)

Track history:

```text
start_date
end_date
is_current
```

---

### 5️⃣ Use Streams in Snowflake

```text
Track row-level changes
```

---

## Real Pipeline

```text
Source
   ↓
S3
   ↓
Glue Job
   ↓
Snowflake (MERGE / Streams)
```

---

## Short Interview Answer

> Glue handles CDC using techniques like timestamp-based filtering, MERGE operations in the target system, and SCD Type 2 for tracking history, since Glue bookmarks only support append-only data.

---

# 3. End-to-End Pipeline Design (Very Important)

## Basic Architecture

```text
Source System
      ↓
S3 (raw data)
      ↓
Glue Crawler
      ↓
Glue Job (transform)
      ↓
Snowflake (COPY INTO / Snowpipe)
      ↓
Final Table
      ↓
Dashboard (BI tools)
```

---

## Step-by-Step Flow

### Step 1 — Ingestion

```text
Source → S3
```

---

### Step 2 — Metadata

```text
Crawler → Data Catalog
```

---

### Step 3 — Transformation

```text
Glue Job → clean + transform
```

---

### Step 4 — Load

```text
Snowflake → COPY INTO / Snowpipe
```

---

### Step 5 — Consumption

```text
BI Tools → dashboards
```

Tools:

* Tableau
* Power BI

---

## Important Points

* Use partitioning
* Use incremental loads
* Handle schema evolution
* Optimize cost

---

## Short Interview Answer

> A typical data pipeline involves ingesting data into S3, using Glue for transformation, loading it into Snowflake using COPY INTO or Snowpipe, and then serving it to BI tools for analytics.

---

# 4. Glue vs Databricks

## Basic Difference

| Feature | Glue           | Databricks    |
| ------- | -------------- | ------------- |
| Type    | Serverless ETL | Data platform |
| Control | Less           | More          |
| Ease    | Easy           | Complex       |
| Cost    | Pay per use    | Cluster-based |

---

## Key Differences

### 1️⃣ Infrastructure

```text
Glue → serverless
Databricks → managed cluster
```

---

### 2️⃣ Flexibility

```text
Glue → limited customization
Databricks → full control
```

---

### 3️⃣ Use Case

| Use Case               | Best Tool  |
| ---------------------- | ---------- |
| Simple ETL             | Glue       |
| Complex ML / pipelines | Databricks |

---

### 4️⃣ Performance

```text
Glue → moderate
Databricks → high performance
```

---

## When to Use What

### Use Glue when:

```text
Simple ETL
Serverless requirement
AWS ecosystem
```

---

### Use Databricks when:

```text
Complex transformations
Streaming pipelines
Machine learning
```

---

## Short Interview Answer

> AWS Glue is a serverless ETL service suitable for simple batch processing, while Databricks is a full data platform offering more flexibility and performance for complex data engineering and machine learning workloads.

---

# 🎯 Final Revision Summary

```text
Glue tuning → partition, Parquet, pushdown
CDC → MERGE, SCD2, timestamps
Pipeline → S3 → Glue → Snowflake → BI
Glue vs Databricks → serverless vs full platform
```

---
