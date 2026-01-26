Perfect 👍
Here are **complete AWS Athena notes in simple English**, **including your doubts clearly answered**, and written **exactly for Amazon interviews**.

---

# 🔎 AWS Athena — COMPLETE NOTES (Simple English + Interview Ready)

Amazon Web Services

![Image](https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2022/08/05/Figure-1.-Serverless-data-archiving-and-retrieval-1024x763.png)

![Image](https://d2908q01vomqb2.cloudfront.net/5b384ce32d8cdef02bc3a139d4cac0a22bb029e8/2021/07/30/Picture1-7.png)

![Image](https://miro.medium.com/1%2AM7LCg5UQZcsw7dfVkpDEfA.png)

---

## 1️⃣ What is AWS Athena?

**AWS Athena** is a **serverless SQL query service** that lets you **query data directly from S3**.

👉 Athena **does not store data**
👉 Athena **does not manage servers**

### One-line interview answer (MEMORIZE)

> *“Athena is a serverless SQL query engine used to analyze data stored in S3.”*

---

## 2️⃣ What kind of operations does Athena give? (YOUR DOUBT CLEARED)

### ✅ Athena is mainly **READ-ONLY**

Athena allows:

* Reading data
* Analyzing data
* Aggregations & joins

Athena does **NOT** allow:

* INSERT
* UPDATE
* DELETE
* MERGE
* Transactions

👉 Athena is **NOT** a database
👉 Athena is a **query engine**

### Interview-safe line

> *“Athena supports read-only analytical SQL operations on S3 data.”*

---

## 3️⃣ Operations Athena Supports (Important)

### 1. SELECT (Most common)

```sql
SELECT * FROM sales;
```

---

### 2. Filtering

```sql
SELECT * FROM sales WHERE year = 2025;
```

---

### 3. Aggregations

```sql
SELECT SUM(amount), COUNT(*) FROM sales;
```

---

### 4. GROUP BY

```sql
SELECT region, SUM(amount)
FROM sales
GROUP BY region;
```

---

### 5. JOIN (READ-only joins)

```sql
SELECT s.order_id, c.name
FROM sales s
JOIN customers c
ON s.customer_id = c.id;
```

---

### 6. CREATE EXTERNAL TABLE (Metadata only)

```sql
CREATE EXTERNAL TABLE sales (...)
LOCATION 's3://bucket/path/';
```

⚠️ This **does NOT create data**, only schema.

---

### 7. CTAS – Create Table As Select ⭐

```sql
CREATE TABLE sales_summary
AS
SELECT region, SUM(amount)
FROM sales
GROUP BY region;
```

👉 Result is written to **S3**
👉 Athena still remains read-only on source

Interview gold line:

> *“CTAS writes query results to S3, not to Athena storage.”*

---

## 4️⃣ What Athena CANNOT do (VERY IMPORTANT)

❌ Update a row
❌ Delete a row
❌ Insert new rows into existing table
❌ Handle transactions

### If interviewer asks:

**“How do you update data queried by Athena?”**

Correct answer:

> *“We use Glue or Spark to rewrite data in S3.”*

---

## 5️⃣ How Athena Works (Simple Flow)

1. Data stored in **S3**
2. Schema stored in **Glue Data Catalog**
3. Athena reads metadata
4. Athena scans files in S3
5. Results returned

👉 Athena **only scans data**, nothing else

---

## 6️⃣ Athena + Glue Data Catalog (VERY IMPORTANT)

* Athena uses **Glue Catalog** for table definitions
* Tables map to **S3 locations**
* Crawlers can auto-create tables

Interview line:

> *“Athena relies on Glue Data Catalog for metadata management.”*

---

## 7️⃣ File Formats (COST & PERFORMANCE)

### ❌ Bad

* CSV
* JSON

### ✅ Best

* **Parquet**
* ORC

Why Parquet?

* Columnar format
* Reads only needed columns
* Less data scanned → less cost

---

## 8️⃣ Partitioning in Athena (CRITICAL)

Athena charges **per data scanned**.

### Example S3 structure

```
s3://analytics-bucket/sales/year=2025/month=01/day=15/data.parquet
```

Query:

```sql
SELECT *
FROM sales
WHERE year = 2025 AND month = 01;
```

👉 Athena scans **only required partitions**

Interview line:

> *“Partition pruning is the biggest Athena cost optimization.”*

---

## 9️⃣ Athena Cost Model (VERY IMPORTANT)

You pay for:

* **Amount of data scanned per query**

Cost reduction checklist:

* Use Parquet
* Partition data
* Avoid SELECT *
* Filter on partition columns
* Use CTAS for repeated queries

---

## 🔟 Athena vs Redshift (COMMON QUESTION)

| Athena         | Redshift            |
| -------------- | ------------------- |
| Serverless     | Cluster-based       |
| Read-only      | Full analytics      |
| Ad-hoc queries | Frequent dashboards |
| Pay per scan   | Pay per cluster     |

Perfect answer:

> *“Athena is for ad-hoc analysis, Redshift is for frequent analytics.”*

---

## 1️⃣1️⃣ Athena vs Glue

| Athena            | Glue                 |
| ----------------- | -------------------- |
| Query engine      | ETL engine           |
| No transformation | Heavy transformation |
| Interactive       | Batch jobs           |

---

## 1️⃣2️⃣ Security in Athena

* IAM roles control access
* S3 bucket policies apply
* Supports encryption

Interview line:

> *“Athena access is controlled using IAM and S3 policies.”*

---

## 1️⃣3️⃣ Common Athena Mistakes (Say this!)

❌ Using Athena for ETL
❌ No partitioning
❌ CSV in analytics layer
❌ Re-running heavy queries repeatedly
❌ Thinking Athena updates data

---

## 1️⃣4️⃣ Amazon Interview Questions (With Correct Answers)

**Q: Is Athena read-only?**
Yes, it only reads data.

**Q: Can Athena modify S3 data?**
No.

**Q: Where does Athena store data?**
It doesn’t. Data stays in S3.

**Q: How to change data queried by Athena?**
Using Glue or Spark.

**Q: Does Athena need Glue?**
Yes, for metadata.

---

## 🎯 Bar Raiser Summary (MEMORIZE)

> *“I use AWS Athena for ad-hoc, read-only analytics on S3 data, optimizing cost through Parquet and partitioning, and managing schemas using Glue Data Catalog.”*

---

## 🧠 FINAL MEMORY HOOK

> **Athena = SQL on S3 (READ ONLY)**

---
