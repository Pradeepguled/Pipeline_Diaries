Below are **complete AWS DynamoDB notes in simple English**, **Amazon-interview focused**, and **easy to remember** — same clean style as S3, IAM, Lambda, Glue, Athena, Redshift.

---

# ⚡ AWS DynamoDB — Complete Notes (Simple English + Interview Q&A)

Amazon Web Services

![Image](https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2024/08/20/fig5-wesfarmers-queue-1260x593.png)

![Image](https://d2908q01vomqb2.cloudfront.net/887309d048beef83ad3eabf2a79a64a389ab1c9f/2017/02/15/PartitionKey.png)

![Image](https://miro.medium.com/v2/resize%3Afit%3A1400/0%2A1SlVcb63uJqt2Ovb)

![Image](https://imgv2-2-f.scribdassets.com/img/document/460328706/original/0763805b61/1?v=1)

---

## 1️⃣ What is AWS DynamoDB?

**AWS DynamoDB** is a **fully managed NoSQL database** designed for **very fast read and write operations at massive scale**.

In simple words:

> **DynamoDB is used when you need millisecond-level performance and high scalability.**

### One-line interview answer (MEMORIZE)

> *“DynamoDB is a serverless NoSQL key-value database that provides low-latency access at any scale.”*

---

## 2️⃣ When do we use DynamoDB?

Use DynamoDB when:

* You need **very fast reads/writes**
* Data access is by **key**
* Traffic is unpredictable
* High availability is required

Typical use cases:

* Session management
* User profiles
* Metadata store
* Idempotency keys
* Application state

❌ Do NOT use DynamoDB when:

* Complex joins are needed
* Heavy analytics is required
  (→ use Redshift / Athena)

---

## 3️⃣ DynamoDB Data Model (VERY IMPORTANT)

### 🔑 Primary Key

Every table must have a **primary key**.

Two types:

### 1️⃣ Partition Key (Simple primary key)

```text
user_id
```

* Used to distribute data
* Must be unique

---

### 2️⃣ Partition Key + Sort Key (Composite key)

```text
order_id  (partition key)
order_date (sort key)
```

* Partition key → where data is stored
* Sort key → how data is ordered within partition

Interview line:

> *“Partition key decides data distribution, sort key enables range queries.”*

---

## 4️⃣ How DynamoDB Stores Data (Simple)

* Data is spread across multiple partitions
* Based on **partition key hash**
* Automatically scales

👉 You don’t manage servers, disks, or partitions.

---

## 5️⃣ Indexes in DynamoDB (Amazon LOVES THIS)

### 🔹 Global Secondary Index (GSI)

* Different partition key than main table
* Used for alternate access patterns

### 🔹 Local Secondary Index (LSI)

* Same partition key
* Different sort key
* Defined at table creation

Interview line:

> *“Indexes support additional query patterns in DynamoDB.”*

---

## 6️⃣ Read & Write Capacity (Important)

### Two modes:

### 🔹 On-Demand

* Auto scaling
* Pay per request
* Best for unpredictable traffic

### 🔹 Provisioned

* Fixed read/write capacity
* Cheaper for steady traffic

Interview line:

> *“On-demand mode is best when traffic is unpredictable.”*

---

## 7️⃣ Strong vs Eventual Consistency

### Eventual Consistency (Default)

* Faster
* Slight delay

### Strong Consistency

* Always latest data
* Slightly slower

Interview line:

> *“DynamoDB supports both eventual and strong consistency.”*

---

## 8️⃣ DynamoDB vs RDS (VERY COMMON)

| DynamoDB      | RDS              |
| ------------- | ---------------- |
| NoSQL         | SQL              |
| Key-value     | Relational       |
| Serverless    | Server-based     |
| No joins      | Supports joins   |
| Massive scale | Vertical scaling |

Perfect answer:

> *“DynamoDB is used for high-scale, low-latency access, while RDS is for relational data.”*

---

## 9️⃣ DynamoDB in Data Engineering (Real usage)

In data pipelines, DynamoDB is often used for:

* Job status tracking
* Checkpointing
* Idempotency control
* Metadata storage

Example:

> Store processed file names to avoid reprocessing the same file.

---

## 🔟 Security in DynamoDB

* IAM roles & policies
* Encryption at rest
* VPC endpoints
* Fine-grained access control

Interview line:

> *“DynamoDB access is controlled using IAM roles with least privilege.”*

---

## 1️⃣1️⃣ Common DynamoDB Mistakes (Say this!)

❌ Poor partition key choice
❌ Hot partitions
❌ Using DynamoDB for analytics
❌ Overusing GSIs
❌ Treating it like SQL DB

---

## 1️⃣2️⃣ DynamoDB Interview Questions & Answers

**Q: What is DynamoDB?**
A serverless NoSQL key-value database.

**Q: What is a partition key?**
Key used to distribute data.

**Q: What is GSI?**
Secondary index for alternate queries.

**Q: DynamoDB vs RDS?**
NoSQL vs relational.

**Q: Does DynamoDB support joins?**
No.

**Q: Is DynamoDB serverless?**
Yes.

---

## 🎯 Bar Raiser STAR Summary (MEMORIZE)

> *“I used DynamoDB as a low-latency metadata and idempotency store, designing efficient partition keys, enabling GSIs for alternate access patterns, and securing access using IAM roles.”*

---

## 🧠 Final Memory Hook

> **DynamoDB = Key-Value + Millisecond + Massive Scale**

---

