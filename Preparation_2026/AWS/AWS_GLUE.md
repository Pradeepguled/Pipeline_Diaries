
---

# 🧩 AWS Glue — Complete Notes (Simple English + Interview Q&A)

Amazon Web Services

![Image](https://docs.aws.amazon.com/images/glue/latest/dg/images/HowItWorks-overview.png)

![Image](https://d2908q01vomqb2.cloudfront.net/b6692ea5df920cad691c20319a6fffd7a4a766b8/2021/09/22/BDB-1195-image001.png)

![Image](https://docs.aws.amazon.com/images/glue/latest/dg/images/PopulateCatalog-overview.png)

![Image](https://d2908q01vomqb2.cloudfront.net/b6692ea5df920cad691c20319a6fffd7a4a766b8/2023/08/11/bdb-3517-image001.png)

---

## 1️⃣ What is AWS Glue?

**AWS Glue** is a **serverless ETL service** used to **extract, transform, and load data**.

In simple words:

> **Glue is used to clean, transform, and move data at scale using Spark — without managing servers.**

### One-line interview answer

> *“AWS Glue is a serverless Spark-based ETL service used for large-scale data transformations.”*

---

## 2️⃣ Why do we use Glue?

Use Glue when:

* Data is **large**
* Transformations are **heavy**
* You need **Spark**
* You don’t want to manage clusters

❌ Do NOT use Glue for:

* Small validations
* Simple orchestration
  (→ use Lambda instead)

---

## 3️⃣ Main Components of AWS Glue (VERY IMPORTANT)

### 🔹 Glue Job

* Actual ETL code
* Runs on **Apache Spark**
* Written in **PySpark / Scala**

👉 This is where transformation happens.

---

### 🔹 Glue Crawler

* Automatically scans data in S3
* Detects schema
* Creates tables in Glue Catalog

Interview line:

> *“Crawler is for schema discovery, job is for transformation.”*

---

### 🔹 Glue Data Catalog

* Central metadata store
* Used by:

  * Glue
  * Athena
  * Redshift Spectrum

Think of it as:

> **“Hive Metastore for AWS”**

---

### 🔹 DPUs (Data Processing Units)

* Measure of Glue compute
* 1 DPU = 4 vCPU + 16 GB RAM

Interview line:

> *“Glue jobs scale by increasing DPUs.”*

---

## 4️⃣ Glue Job Types

### Spark Jobs (Most common)

* Heavy transformations
* Joins, aggregations, dedupe

### Python Shell Jobs

* Lightweight scripting
* No Spark

Amazon expects:

> *“Most ETL jobs are Spark-based Glue jobs.”*

---

## 5️⃣ Glue Job Execution Flow (Simple)

1. Read data from **S3**
2. Load schema from **Glue Catalog**
3. Transform using Spark
4. Write output back to **S3**
5. Update catalog if needed

---

## 6️⃣ Glue in Data Engineering (Real usage)

Typical pipeline:

* Raw data → S3
* Crawler → detect schema
* Glue job → clean & transform
* Write Parquet to curated layer
* Athena / Redshift → query

Interview line:

> *“Glue is mainly used for batch ETL in the data lake.”*

---

## 7️⃣ Incremental Data Handling in Glue

### Glue Job Bookmarks ⭐

* Track processed data
* Avoid reprocessing old data

Used when:

* Daily/hourly loads
* Append-only data

Interview line:

> *“We use job bookmarks to process only new data.”*

---

## 8️⃣ Glue Performance Optimization (Amazon LOVES this)

### Common optimizations

* Use **Parquet**
* Partition data
* Reduce shuffles
* Repartition before joins
* Increase DPUs carefully
* Avoid too many small files

Golden line:

> *“Increasing DPUs alone doesn’t fix performance — Spark optimization is required.”*

---

## 9️⃣ Glue vs Lambda (VERY COMMON)

| Glue             | Lambda            |
| ---------------- | ----------------- |
| Heavy ETL        | Lightweight logic |
| Spark-based      | No Spark          |
| Minutes–hours   | Seconds–minutes  |
| Batch processing | Event-based       |

Perfect answer:

> *“Glue is for transformation, Lambda is for orchestration.”*

---

## 🔟 Glue vs EMR (Amazon favorite)

| Glue           | EMR             |
| -------------- | --------------- |
| Serverless     | Cluster-based   |
| Less control   | Full control    |
| Easy to manage | More tuning     |
| Pay per job    | Pay per cluster |

Interview line:

> *“Glue is preferred for standard ETL, EMR for complex or long-running Spark workloads.”*

---

## 1️⃣1️⃣ IAM Role in Glue (VERY IMPORTANT)

* Glue uses **IAM Role**
* Role permissions:

  * Read/write S3
  * Access logs
  * Access KMS if encrypted

Interview line:

> *“Glue securely accesses data using IAM roles, not access keys.”*

---

## 1️⃣2️⃣ Error Handling & Monitoring

* Logs → CloudWatch
* Job retries
* Failures tracked in Glue console
* Alerts via CloudWatch + SNS

---

## 1️⃣3️⃣ Common Glue Mistakes (Say in interviews)

❌ Too many small files
❌ No partitioning
❌ Blindly increasing DPUs
❌ Using CSV in curated layer
❌ No job bookmarks

---

## 1️⃣4️⃣ AWS Glue Interview Questions (Simple Answers)

**Q: What is AWS Glue?**
Serverless Spark-based ETL service.

**Q: What is a Glue Crawler?**
Automatically detects schema and creates tables.

**Q: What are DPUs?**
Units of compute for Glue jobs.

**Q: How do you handle incremental data?**
Using Glue job bookmarks.

**Q: Where does Glue store metadata?**
Glue Data Catalog.

**Q: Glue vs EMR?**
Glue = serverless ETL, EMR = managed clusters.

---

## 1️⃣5️⃣ Bar Raiser STAR Summary (MEMORIZE)

> *“I used AWS Glue to build serverless Spark ETL pipelines, handling incremental loads with job bookmarks, optimizing performance through partitioning and Parquet, and securely accessing data using IAM roles.”*

---

## 🧠 Final Memory Hook

> **Glue = Serverless Spark + ETL + Catalog + DPUs**
