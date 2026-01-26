
---

# 🔍 AWS Glue Crawler — Deep Notes (Simple English + Example)

Amazon Web Services

![Image](https://d2908q01vomqb2.cloudfront.net/b6692ea5df920cad691c20319a6fffd7a4a766b8/2023/08/11/bdb-3517-image001.png)

![Image](https://docs.aws.amazon.com/images/glue/latest/dg/images/PopulateCatalog-overview.png)

![Image](https://content.cloudthat.com/resources/wp-content/uploads/2025/05/glue.webp)

---

## 1️⃣ What is an AWS Glue Crawler?

**AWS Glue Crawler** is used to **automatically detect schema** from data stored in **S3** (or JDBC sources) and **create/update tables in Glue Data Catalog**.

### In simple words:

> **Crawler looks at data, understands its structure, and creates table metadata.**

---

## 2️⃣ What does a Glue Crawler actually do?

A crawler:

1. Reads files from S3
2. Detects:

   * File format (CSV, JSON, Parquet)
   * Columns & data types
   * Partitions
3. Creates or updates:

   * Database
   * Tables
   * Partition metadata

🚫 **Crawler does NOT transform data**
🚫 **Crawler does NOT move data**

---

## 3️⃣ Glue Crawler vs Glue Job (VERY COMMON)

| Crawler                 | Job                 |
| ----------------------- | ------------------- |
| Schema discovery        | Data transformation |
| Metadata only           | Actual ETL          |
| No Spark transformation | Spark-based         |
| Creates tables          | Writes data         |

Interview-ready line:

> *“Crawler is for schema discovery, Glue job is for transformation.”*

---

## 4️⃣ When should you use a Crawler?

Use a crawler when:

* New data source is added
* Schema is unknown
* Partition structure changes
* New files arrive daily

❌ Avoid crawler when:

* Schema is fixed and stable
* Performance is critical (manual schema is faster)

---

## 5️⃣ Real Example (NCCT-style – VERY IMPORTANT)

### 📂 S3 Raw Data Structure

```
s3://ncct-raw/claims/year=2025/month=01/day=15/claims.parquet
```

---

### 🛠️ Step-by-step: How Crawler is used

### Step 1: Create Crawler

* Data store: S3
* Path: `s3://ncct-raw/claims/`
* IAM Role: Glue service role
* Database: `ncct_raw_db`

---

### Step 2: Run Crawler

Crawler scans files and:

* Detects columns like:

  * claim_id (string)
  * member_id (string)
  * claim_amount (double)
  * claim_date (date)
* Detects partitions:

  * year
  * month
  * day

---

### Step 3: Output in Glue Data Catalog

Crawler creates:

```
Database: ncct_raw_db
Table: claims
Partitions: year, month, day
```

Now:

* Glue jobs can read this table
* Athena can query it directly

---

## 6️⃣ Schema Evolution Handling (VERY IMPORTANT)

Crawler can:

* Add new columns automatically
* Update partition metadata

Example:

* New column added: `provider_type`
* Crawler updates table schema

Interview line:

> *“Glue crawler helps handle schema evolution by automatically updating metadata.”*

⚠️ Best practice:

* Review schema changes
* Avoid breaking downstream jobs

---

## 7️⃣ Crawler Configuration Options (Amazon checks this)

### Schema change policy

* Add new columns
* Ignore changes
* Log changes only

### Partition behavior

* Inherit from folder structure
* Detect new partitions

---

## 8️⃣ Performance & Cost Considerations

* Crawlers scan **entire data path**
* Too many files → slow crawler
* Frequent runs increase cost

Best practices:

* Run crawler **only when needed**
* Use crawlers mainly for **raw layer**
* Avoid frequent crawler runs on curated data

Interview line:

> *“We don’t run crawlers frequently on large curated datasets to avoid cost and latency.”*

---

## 9️⃣ Common Mistakes with Crawlers (Say in interview)

❌ Running crawler before every job
❌ Using crawler for transformation
❌ Crawling huge historical data repeatedly
❌ Letting crawler change schema without review

---

## 🔟 Amazon Interview Questions on Glue Crawler

### Q1. What is Glue Crawler?

> A service that automatically discovers schema and creates tables in Glue Catalog.

---

### Q2. Does crawler transform data?

> No. It only creates metadata.

---

### Q3. How does crawler handle partitions?

> It detects partitions from S3 folder structure.

---

### Q4. When should you avoid crawler?

> When schema is stable or dataset is very large.

---

### Q5. How do you handle schema changes safely?

> Configure crawler to add new columns only and validate downstream jobs.

---

## 🎯 Bar Raiser STAR Line (MEMORIZE)

> *“I used Glue crawlers to automatically discover schema and partitions in raw S3 data, keeping the Glue Catalog in sync and enabling Glue jobs and Athena queries without manual metadata management.”*

---

## 🧠 Memory Hook

> **Crawler = Schema + Metadata + Partitions**

---
