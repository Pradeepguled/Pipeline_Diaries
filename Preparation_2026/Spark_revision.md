# 📘 Apache Spark – Complete Revision Notes (Interview + Practical)

## 1. What is Apache Spark?

:contentReference[oaicite:0]{index=0} is a distributed data processing engine designed to process large-scale data efficiently using parallelism and in-memory computation.

### Why Spark is fast

- Processes data in memory
- Executes tasks in parallel across machines
- Optimizes execution plans automatically

**Interview-ready answer:**
Spark is a distributed data processing engine that enables fast processing of large datasets using in-memory computation and parallel execution.

---

## 2. Spark Architecture

### Driver

- Acts as the brain of Spark
- Creates the execution plan (DAG)
- Schedules tasks
- Collects results from executors

### Executor

- JVM process running on worker nodes
- Executes tasks
- Stores cached data
- Handles shuffle read and write

### Cluster Manager

- Allocates resources
- Examples: YARN, Kubernetes, Standalone

**Interview-ready answer:**
The driver coordinates the job, executors perform computations, and the cluster manager allocates resources.

---

## 3. RDDs (Resilient Distributed Datasets)

### What is an RDD?

- Low-level distributed data structure
- Immutable
- Fault tolerant
- Data split into partitions

### Immutability

RDDs cannot be modified. Every transformation creates a new RDD.

### Why immutability matters

- Safe parallel execution
- Enables fault recovery using lineage

**Interview-ready answer:**
RDDs are immutable distributed collections that provide fault tolerance through lineage.

---

## 4. DataFrames & Spark SQL

### DataFrame

- Structured data with schema
- Built on top of RDDs
- Optimized using Catalyst Optimizer

### Why DataFrames over RDDs

- Less code
- Automatic optimizations
- Better performance

**Interview-ready answer:**
DataFrames provide a higher-level API with schema information that allows Spark to optimize queries automatically.

---

## 5. Transformations vs Actions

### Transformations

- Lazy operations
- Build logical execution plan
- Examples: map, filter, select, groupBy, join

### Actions

- Trigger execution
- Examples: count, collect, show, write

**Interview-ready answer:**
Transformations define computation lazily, while actions trigger execution.

---

## 6. Lazy Evaluation & DAG

### Lazy Evaluation

Spark delays execution until an action is called, allowing it to optimize the full execution plan.

### DAG (Directed Acyclic Graph)

Logical execution graph representing transformations, later converted into stages.

**Interview-ready answer:**
Lazy evaluation allows Spark to optimize execution by analyzing the entire DAG before running the job.

---

## 7. Partitions, Tasks, and Stages

### Partition

Small chunk of data that enables parallelism.

### Task

Unit of work on one partition, executed inside an executor.

### Stage

Group of tasks that can run without shuffle. Shuffle creates a new stage.

**Interview-ready answer:**
Spark divides jobs into stages based on shuffle boundaries, and each stage contains tasks that process partitions.

---

## 8. Shuffle (Critical Concept)

### What is Shuffle?

Redistribution of data across executors so that rows with the same key end up together.

### Causes of Shuffle

- groupBy
- join
- distinct
- orderBy
- repartition

### Why shuffle is expensive

- Disk I/O
- Network transfer
- Sorting
- High memory usage

**Interview-ready answer:**
Shuffle redistributes data across executors and is expensive due to disk and network I/O.

---

## 9. Narrow vs Wide Transformations

### Narrow Transformations

- No shuffle
- Data stays in the same partition
- Examples: map, filter

### Wide Transformations

- Shuffle required
- Data moves across partitions
- Examples: groupBy, join

**Interview-ready answer:**
Wide transformations require shuffle, while narrow transformations do not.

---

## 10. reduceByKey vs groupByKey

### reduceByKey

- Performs local aggregation before shuffle
- Less data movement
- More efficient

### groupByKey

- Shuffles all data first
- High memory usage
- Avoid in production

**Interview-ready answer:**
reduceByKey is preferred because it reduces data locally before shuffle.

---

## 11. Data Skew

### What is data skew?

When some keys have much more data than others, causing one task to take much longer.

### Problems

- Slow jobs
- OOM errors
- Job stuck at 99%

### Solutions

- Broadcast join
- Salting
- AQE
- Separate heavy keys

**Interview-ready answer:**
Data skew occurs when uneven data distribution causes performance bottlenecks during shuffle.

---

## 12. Repartition vs Coalesce

### Repartition

- Causes shuffle
- Used to balance data
- Used before joins or aggregations

### Coalesce

- Reduces partitions without shuffle
- Used before writing data to avoid small files

**Interview-ready answer:**
Repartition balances data with shuffle, while coalesce efficiently reduces partitions.

---

## 13. Partitioning vs Bucketing

### Partitioning

- Creates folders based on column values
- Helps filtering
- Does not help joins

Example:
year=2024/, year=2025/

### Bucketing

- Uses hash of a column
- Fixed number of buckets
- Helps joins by reducing shuffle

Example:
bucket_0, bucket_1, bucket_2

**Interview-ready answer:**
Partitioning optimizes data reads, while bucketing optimizes joins.

---

## 14. Hash of a Column

Hashing converts a column value into a number to determine which bucket the row belongs to. Same key always maps to the same bucket.

**Interview-ready answer:**
Hashing ensures consistent placement of keys into buckets for efficient joins.

---

## 15. Spark Join Execution

### Broadcast Join

- One table is small
- Small table sent to all executors
- No shuffle

### Shuffle Join

- Both tables are large
- Data shuffled by join key
- Expensive

**Interview-ready answer:**
Spark chooses join strategies based on data size, preferring broadcast joins when possible.

---

## 16. Broadcast Variables

### What are they?

Read-only variables sent once to all executors.

### Use cases

- Lookup tables
- Small configuration data

**Interview-ready answer:**
Broadcast variables efficiently share small read-only data across executors.

---

## 17. Accumulators

### What are they?

Write-only shared variables used to collect metrics from executors.

### Use cases

- Counters
- Debugging
- Monitoring

**Interview-ready answer:**
Accumulators aggregate information from executors back to the driver.

---

## 18. Cache vs Persist

### cache()

Stores data in memory.

### persist()

Allows different storage levels (memory + disk).

Use caching only when data is reused multiple times.

**Interview-ready answer:**
Caching improves performance when reused, but unnecessary caching wastes memory.

---

## 19. File Formats

- CSV: Slow, no schema
- JSON: Semi-structured
- Parquet: Columnar, compressed, fast
- ORC: Similar to Parquet

**Interview-ready answer:**
Columnar formats like Parquet improve performance by reducing I/O.

---

## 20. Spark Cluster Configuration (Interview Level)

### Key configurations

- Number of executors
- Executor cores
- Executor memory
- Driver memory
- spark.sql.shuffle.partitions

### Common tuning ideas

- Moderate cores per executor (3–5)
- Tune shuffle partitions based on data size
- Fix skew before increasing memory

**Interview-ready answer:**
Cluster configuration should balance parallelism, memory usage, and shuffle performance.

---

## 21. Spark UI (Debugging)

Use Spark UI to:

- Identify slow stages
- Check shuffle read/write
- Detect skew via task duration
- Inspect join strategies

**Interview-ready answer:**
I use Spark UI to analyze shuffle-heavy stages and performance bottlenecks.

---

## 22. Common Situation-Based Interview Questions

### Job is slow

Check Spark UI → identify shuffle → check skew → optimize joins or partitions.

### Job stuck at 99%

Usually caused by data skew.

### OOM error

Reduce shuffle, fix skew, avoid collect(), then increase memory if needed.

### Too many small files

Use coalesce before write or file compaction.

---

# 📘 Spark Cluster Configuration & Situation-Based Interview Questions

---

## 23. Spark Cluster Configuration (Interview + Practical)

Spark performance depends heavily on **how the cluster is configured**, not just code.

Interviewers do NOT expect DevOps-level tuning, but they DO expect you to understand **trade-offs**.

---

### 23.1 Core Cluster Components (Quick Recall)

- **Driver** – Plans and coordinates the job
- **Executors** – Perform actual computation
- **Cores** – Control parallelism
- **Memory** – Used for shuffle, joins, caching
- **Partitions** – Define how work is split

---

### 23.2 Important Spark Configuration Parameters

#### 1. Number of Executors

Controls how many JVM worker processes run.

- More executors → more parallelism
- Too many → scheduling overhead

**Interview-ready answer:**
Choosing the right number of executors helps balance parallelism and overhead.

---

#### 2. Executor Cores

Controls how many tasks an executor can run in parallel.

- Recommended: **3–5 cores per executor**
- Too many cores → GC pressure and uneven execution

**Interview-ready answer:**
Using fewer cores per executor avoids GC overhead and improves task stability.

---

#### 3. Executor Memory

Used for:

- Shuffle
- Joins
- Cache

Issues:

- Low memory → disk spill → slow jobs
- Very high memory → GC overhead

**Interview-ready answer:**
Most memory issues are caused by shuffle and skew, not lack of total memory.

---

#### 4. Driver Memory

Used for:

- DAG creation
- collect()
- Job metadata

⚠️ Driver OOM usually happens due to `collect()` on large datasets.

**Interview-ready answer:**
Driver memory issues usually indicate incorrect usage like collecting large results.

---

#### 5. spark.sql.shuffle.partitions

Default = **200**

Controls number of partitions created after shuffle.

- Small data → reduce it
- Large data → increase it

**Interview-ready answer:**
I tune shuffle partitions based on data size to balance task size and parallelism.

---

## FINAL 60-SECOND SUMMARY (MEMORIZE)

Spark processes data in parallel using executors and partitions. Transformations are lazily evaluated and organized into stages separated by shuffle boundaries. Performance issues usually come from shuffle, skew, or poor partitioning and can be optimized using broadcast joins, repartitioning, bucketing, and proper cluster tuning.
