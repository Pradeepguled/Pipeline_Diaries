
---

# Apache Kafka – Crisp Notes (Data Engineer)

## 1️⃣ What is Kafka?

**Apache Kafka** is a **distributed event streaming platform**.

👉 In simple words:
Kafka is like a **high-speed, fault-tolerant message log** where systems **publish events** and **other systems consume them**.

**Used for:**

* Real-time data ingestion
* Streaming pipelines
* Decoupling systems
* Event-driven architectures

---

## 2️⃣ Core Kafka Concepts (Must know)

### 🔹 Topic

* A **category / stream of events**
* Example: `customer_events`, `order_events`

Think of it as a **table**, but:

* No updates
* Only appends (immutable)

---

### 🔹 Producer

* Application that **writes data to Kafka**
* Example: app sending customer updates

```text
App → Kafka Topic
```

---

### 🔹 Consumer

* Application that **reads data from Kafka**
* Example: Spark job, Kafka Connect, Flink

```text
Kafka Topic → Consumer
```

---

### 🔹 Partition (Very Important)

* A topic is split into **partitions**
* Each partition is an **ordered log**

Example:

```
Topic: customer_events
Partitions: P0 | P1 | P2
```

✔ Parallelism
✔ Scalability
✔ Ordering is **guaranteed only within a partition**

---

### 🔹 Offset

* Position of a message inside a partition
* Kafka stores messages as:

```text
(topic, partition, offset)
```

Consumers track offsets to know **what they have read**.

---

## 3️⃣ Kafka Architecture

```
Producer
   ↓
Kafka Broker 1 ── Partition 0
Kafka Broker 2 ── Partition 1
Kafka Broker 3 ── Partition 2
   ↓
Consumers
```

### 🔹 Broker

* Kafka server that stores data
* A Kafka cluster has **multiple brokers**

---

### 🔹 Replication

* Each partition has replicas
* One **leader**, others are **followers**

If leader fails → follower becomes leader
➡ **High availability**

---

## 4️⃣ Consumer Groups (Very Important)

* Consumers read as a **group**
* Each partition is read by **only one consumer in a group**

Example:

```
Topic has 3 partitions
Consumer group has 3 consumers
→ Each consumer reads 1 partition
```

✔ Horizontal scaling
✔ No duplicate reads inside same group

---

## 5️⃣ Delivery Semantics

### 🔹 At-most-once

* Message may be lost
* No duplicates

### 🔹 At-least-once (Most common)

* Message delivered **at least once**
* Duplicates possible

### 🔹 Exactly-once

* Harder
* Needs idempotent producers + transactional consumers

👉 **Kafka → S3 → Snowflake = usually at-least-once**
→ handle dedupe downstream

---

## 6️⃣ Kafka Storage Model

* Kafka **stores data on disk**
* Messages retained by:

  * Time (`7 days`)
  * Size (`100GB`)
* Consumers can **replay data**

Kafka ≠ traditional queue
Kafka = **durable event log**

---

## 7️⃣ Kafka Connect (Real projects)

Kafka Connect is used to **move data in/out of Kafka** without writing code.

### 🔹 Source Connector

* Pulls data **into Kafka**
* Example:

  * MySQL → Kafka
  * S3 → Kafka

### 🔹 Sink Connector

* Pushes data **out of Kafka**
* Example:

  * Kafka → S3
  * Kafka → Snowflake
  * Kafka → Elasticsearch

👉 **Kafka → S3 via S3 Sink** (your previous question)

---

## 8️⃣ Schema Management

### Why schema matters

* Producers change fields
* Consumers may break

### Solution: **Schema Registry**

* Avro / Protobuf / JSON Schema
* Enforces compatibility rules:

  * Backward
  * Forward
  * Full

👉 Very important in enterprise pipelines

---

## 9️⃣ Kafka vs Traditional Systems

| Kafka           | DB / Queue        |
| --------------- | ----------------- |
| Append-only     | Update/delete     |
| Replay possible | No replay         |
| High throughput | Limited           |
| Distributed     | Often centralized |

---

## 🔟 Kafka in AWS (Interview Gold)

* **MSK** = Managed Kafka
* Used when:

  * High throughput
  * Many consumers
  * Need replay
* Often paired with:

  * Kafka Connect → S3
  * Spark/Flink → S3/Snowflake

---

## 1️⃣1️⃣ Common Kafka Use Cases

* Application logs
* CDC (DB changes)
* Clickstream data
* IoT events
* ML feature pipelines

---

## 1️⃣2️⃣ Common Problems & Fixes

| Problem           | Solution                   |
| ----------------- | -------------------------- |
| Small files in S3 | Batch writes               |
| Duplicate events  | Dedupe key                 |
| Consumer lag      | Scale consumers            |
| Ordering issue    | Same key → same partition |
| Schema breaking   | Schema Registry            |

---

## 1️⃣3️⃣ How to explain Kafka in interview (1-liner)

> “Kafka is a distributed event streaming platform that acts as a durable, scalable log for real-time data pipelines and decoupled systems.”

---

## 1️⃣4️⃣ Kafka → S3 → Snowflake (One-line summary)

> Producers publish events → Kafka stores & replicates → Kafka Connect batches and writes to S3 → Snowpipe loads into Snowflake → transformations happen downstream.

---
