## ✅ Scenario: Spark batch job suddenly slow (no code change)

**Situation**
Daily Spark job usually finishes in **30 min**. Today it’s taking **2 hours**. No code change. SLA is at risk.

When there is no code change, in production it’s usually **data changed** (size/skew), or **environment changed** (cluster/resources).

---

# 1️⃣ Spark / Batch Technical Handling (Step-by-step)

## Step 1 — Confirm it’s not an infrastructure issue

Before diving into code/data, I check quick basics:

* Did the job get the **same cluster size** as usual?
* Any **spot instance loss / node issues**?
* Any other heavy jobs running causing **resource contention**?

✅ If cluster/resources are smaller, I fix that first (otherwise tuning won’t help).

---

## Step 2 — Use Spark UI to pinpoint where time increased (MOST IMPORTANT)

I open **Spark UI** and do this in order:

### A) Jobs / Stages tab

* Find the stage that is consuming most time.
* Compare with previous successful run if available.

### B) Look for these patterns in the slow stage

#### Pattern 1: “Few tasks are extremely slow”

* 90% tasks finish fast
* 1–5 tasks run for very long time
  ➡️ This is almost always **data skew**

#### Pattern 2: “All tasks are slow”

* Every task is slow
  ➡️ Likely **not enough partitions**, **huge shuffle**, or **I/O bottleneck**

### C) Check Shuffle metrics (key interview point)

In the slow stage, check:

* **Shuffle Read size**
* **Shuffle Write size**
  If shuffle size is high → join/groupBy is expensive today.

### D) Executors tab

Check:

* **GC time very high** → memory pressure
* **Spill to disk high** → shuffle too big / partitions too large
* **Failed executors** → instability / OOM

---

## Step 3 — Validate data change (most common root cause)

Since no code change, I verify:

* Input **file size / row count** higher today
* Number of input files changed (too many small files?)
* Key distribution changed (skewed join key like `customer_id`, `device_id`, etc.)

✅ Quick debug queries:

* `count()` (or sample counts)
* Top keys frequency (to detect skew)

---

# 2️⃣ Fixes I apply (based on what Spark UI shows)

## Fix A — If issue is “Not enough parallelism” (large data, fewer partitions)

**Symptoms**

* All tasks slow
* Stage has low number of partitions
* CPU under-utilized

**Fix**

* Increase shuffle partitions:

```python
spark.conf.set("spark.sql.shuffle.partitions", 400)  # example
```

* Repartition before heavy join/groupBy:

```python
df = df.repartition(400, "join_key")
```

✅ Why: More partitions = more parallel tasks = faster completion (until optimal point).

---

## Fix B — If issue is “Data skew” (few tasks slow)

**Symptoms**

* One/few tasks take very long
* Spark UI shows one partition has huge input size

**Fix options (choose depending on setup):**

### Option 1: Turn on AQE + skew join handling (best quick win)

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
```

### Option 2: Salting technique (best “senior” interview answer)

* Add a random salt to distribute hot keys
* Join on (key + salt)

✅ This spreads one huge key across many partitions.

---

## Fix C — If issue is “Huge shuffle” due to join

**Symptoms**

* Shuffle read/write extremely high
* Join stage dominates time

**Fix**

* Broadcast small dimension tables:

```python
from pyspark.sql.functions import broadcast
fact.join(broadcast(dim), "key")
```

* Push filters early (reduce data before join)
* Select only required columns (drop wide columns early)

✅ Why: Broadcast eliminates shuffle for that join.

---

## Fix D — If issue is “Too many small files” (I/O overhead)

**Symptoms**

* Tasks spend time in reading
* Lots of small input partitions
* High scheduling overhead

**Fix**

* Compact upstream files (daily compaction job)
* Increase file partition size:

```python
spark.conf.set("spark.sql.files.maxPartitionBytes", 268435456)  # 256MB
```

---

## Fix E — If issue is “Memory pressure / spill” (GC high, disk spill high)

**Symptoms**

* Executors show high GC time
* Spill to disk is high
* Sometimes near-OOM

**Fix**

* Reduce shuffle by tuning partitions (not too small, not too big)
* Avoid caching huge datasets
* Persist carefully:

```python
df.persist(StorageLevel.MEMORY_AND_DISK)
```

* Break the job into stages (write intermediate results if needed)

---

# 3️⃣ Prevention (what I do after stabilizing today’s run)

This part makes you sound **senior**.

✅ I add:

* Alert on input size spike (e.g., +50% vs average)
* Data skew check (top key frequency)
* Spark metrics monitoring:

  * shuffle size
  * stage duration
  * GC time
* Runbook entry: “If slow → check skew/shuffle first”

---

# 4️⃣ Managerial / Communication Handling (simple & strong)

While debugging, I message stakeholders:

> “Job is running slow due to higher data volume / skew today. No data loss risk. I’m tuning partitions and join strategy. New ETA: X.”

After resolution:

> “Root cause was data pattern change. We added monitoring + safeguards so it won’t surprise us again.”

---

# ✅ NCCT / Glassbeam-style connection (how you can say it)

> “In my pipelines, even when code is stable, daily input can change a lot. So I always start with Spark UI, identify skew/shuffle, then fix partitioning or join strategy. That approach keeps the SLA stable.”

---

---

## ✅ Q2: Month-end Spark batch job works daily but fails / misses SLA on month-end. How do you handle end-to-end?

### How I answer (high-level)

I handle it in  **3 phases** :

1. **Stabilize today’s run** (meet SLA, avoid data loss)
2. **Find the true root cause** (Spark UI + data analysis)
3. **Permanent fix** (design + monitoring so month-end becomes predictable)

---

# 1️⃣ Phase 1: Stabilize today’s month-end run (Immediate recovery)

### Step 1 — Confirm it’s not a cluster/environment issue

Before tuning Spark, I verify:

* Same cluster size as usual?
* Any spot interruptions / node failures?
* Any other heavy jobs running causing contention?

If resources are reduced or unstable, I fix that first because tuning won’t help much.

---

### Step 2 — Check Spark UI to locate where the job is stuck

In  **Spark UI → Stages** , I find the stage consuming most time / failing.

I look for these patterns:

#### Pattern A: Only few tasks are extremely slow

* 95% tasks finish
* 1–5 tasks take forever
  ✅ This screams **data skew**

#### Pattern B: All tasks are slow

* each task is slow
  ✅ Likely  **not enough parallelism** ,  **huge shuffle** , or **I/O bottleneck**

#### Pattern C: Executors failing / OOM / high GC / spill

✅ This is **memory pressure from shuffle + big partitions + skew**

---

### Step 3 — Apply the right quick fix (based on pattern)

## ✅ If SLA miss due to overall load (parallelism problem)

Month-end input is bigger, so I increase parallelism:

* Increase shuffle partitions:

```python
spark.conf.set("spark.sql.shuffle.partitions", 800)
```

* Repartition before heavy join/groupBy:

```python
df = df.repartition(800, "join_key")
```

**Why:** more partitions → smaller per-task workload → faster and less memory pressure.

---

## ✅ If one/few tasks are slow (data skew)

Month-end often creates skew on business keys (customer/account/device).

Fastest win:

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
```

If skew is severe, I do  **salting** :

* Add salt to the skewed key to spread hot keys across partitions
* Join on (key + salt)

**Why:** one hot key becomes many smaller chunks → tasks become balanced.

---

## ✅ If failure is OOM / ExecutorLost

I fix in the correct order (senior style):

1. Reduce data early

* select only needed columns
* filter early before join/groupBy

2. Reduce shuffle

* broadcast small dimension tables:

```python
from pyspark.sql.functions import broadcast
fact.join(broadcast(dim), "key")
```

3. Right-size partitions

* ensure partitions are not too large
* increase shuffle partitions if needed

4. Persist carefully

* don’t blindly cache huge datasets
* use `MEMORY_AND_DISK` only if reused

5. Only if still needed → adjust executor memory/cores

**Key point to say:**

> “I don’t start by increasing memory. I reduce shuffle and skew first.”

---

## ✅ If issue is too many small files (read overhead)

Month-end sometimes reads massive number of small files → slow listing/reading.

Fix:

```python
spark.conf.set("spark.sql.files.maxPartitionBytes", 268435456)  # 256MB
```

And long-term: add **compaction** job.

---

# 2️⃣ Phase 2: Identify root cause clearly (RCA)

After stabilizing, I confirm why month-end is special:

* Data volume spike (2x–10x)
* Skew increase (top keys dominate)
* Shuffle increase (joins/aggregations heavier)
* Small files explosion (read overhead)
* Different business logic triggered only at month-end (month-end close, adjustments)

I capture proof from:

* Spark UI screenshots/metrics (stage time, shuffle size, skewed tasks)
* Input size stats from storage

---

# 3️⃣ Phase 3: Permanent fix so month-end never surprises again

This is where you sound senior.

## ✅ Best design change: Pre-aggregate daily, not monthly recompute

Instead of month-end doing huge full scans:

* Daily job produces **daily aggregates** (small, clean)
* Month-end job aggregates daily results (lightweight)

This converts month-end from “TB heavy run” to “small rollup job”.

## ✅ Calendar-aware scaling + separate config

* Month-end is predictable → use a  **month-end Spark config** :
  * higher shuffle partitions
  * more executors
  * different instance types if needed

## ✅ Monitoring guardrails

* Alert if input volume > threshold
* Skew detection: top-key frequency spike
* Alert on shuffle size/stage duration/GC time

---

# 4️⃣ Managerial communication (what I say during incident)

During incident:

> “Month-end load is higher and it’s causing heavy shuffle / skew. No data loss risk. I’m applying tuning and scaling. ETA is X.”

After fix:

> “Root cause was month-end data spike + skew. We’ve added month-end config + monitoring and redesigned rollups so it stays stable.”

---

# ✅ NCCT/Glassbeam-style connection (your line)

> “In my pipelines, month-end has higher volume and a few entities dominate the data, which creates skew. I use Spark UI to confirm skew/shuffle, fix with AQE/salting and partition tuning, and long-term I pre-aggregate daily so month-end is always SLA-safe.”

---

## ✅ Q3: Spark batch job fails with Executor OOM / ExecutorLostFailure after running for some time. How do you debug and fix it?

### What this usually means

`ExecutorLostFailure` / OOM is almost never “random”. It usually happens because of:

* **Huge shuffle** (joins/groupBy)
* **Data skew** (one partition becomes massive)
* **Partitions too large** (each task holds too much data)
* **Caching big DF** accidentally
* **Too many columns / wide rows**
* Occasionally: cluster/node issues

I handle it in a very structured way.

---

# 1️⃣ Spark / Batch Technical Handling (Step-by-step)

## Step 1 — Confirm exact failure signature (logs + Spark UI)

### A) Check driver logs / YARN/EMR/Databricks logs

Look for:

* `java.lang.OutOfMemoryError: Java heap space`
* `GC overhead limit exceeded`
* `Container killed by YARN for exceeding memory`
* `ExecutorLostFailure`

This tells me:  **heap OOM vs off-heap vs container limit** .

### B) Spark UI → Executors tab (most useful)

I check:

* Which executors died? (one or many)
* **GC time %** (if very high → memory pressure)
* **Shuffle spill (memory/disk)** (if high → shuffle too big)
* **Input size per task** (if one task has huge input → skew)

### C) Spark UI → Stages tab

Find the stage where failure happened:

* Usually a **join** or **aggregation** stage
* Look for wide transformations: `groupBy`, `distinct`, `orderBy`, `join`

---

## Step 2 — Identify which pattern it matches

### ✅ Pattern A: OOM happens during join/groupBy + shuffle is huge

Cause: wide transformation creating massive shuffle.

### ✅ Pattern B: Only a few executors die repeatedly

Cause: **skew** (those executors got hot partitions).

### ✅ Pattern C: OOM happens after caching

Cause: cached DF too large or wrong storage level.

### ✅ Pattern D: Many small partitions but still OOM

Cause: wide rows / too many columns / bad serialization.

---

# 2️⃣ Fixes (in the right order — this is what seniors do)

## Fix 1 — Reduce data early (most important and safest)

Before any join or groupBy:

* **Select only required columns**
* **Filter as early as possible**

Example mindset:

> “If I can remove 30% rows before shuffle, I save huge memory.”

---

## Fix 2 — Fix skew if present (very common reason for executor loss)

### How I confirm skew

Spark UI shows:

* some tasks have much larger input size
* those tasks run longer / fail

### Fix options

**Option A: AQE Skew Join**

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
```

**Option B: Salting technique**

* add salt for hot keys
* join using (key + salt)

This spreads one huge key across many partitions and avoids one executor dying.

---

## Fix 3 — Right-size partitions (avoid huge partitions causing OOM)

If partitions are too large, each task holds too much data in memory.

### What I do:

* Increase shuffle partitions:

```python
spark.conf.set("spark.sql.shuffle.partitions", 600)
```

* Repartition before heavy operations:

```python
df = df.repartition(600, "join_key")
```

✅ Goal: keep partition sizes around **128–256 MB** for stable tasks.

---

## Fix 4 — Reduce shuffle cost for joins

If one side is small → broadcast it:

```python
from pyspark.sql.functions import broadcast
fact.join(broadcast(dim), "key")
```

✅ Broadcasting removes shuffle for that join → big memory saving.

---

## Fix 5 — Be careful with caching/persisting

Common mistake: `cache()` huge DataFrame and then multiple transformations.

### Better:

* Cache only if reused multiple times
* Use:

```python
df.persist(StorageLevel.MEMORY_AND_DISK)
```

* Unpersist when done:

```python
df.unpersist()
```

---

## Fix 6 — If still failing, then tune resources (last step)

Only after fixing skew/shuffle:

* Increase executor memory
* Reduce executor cores (to reduce per-executor memory pressure)
* Increase number of executors (more parallelism)

✅ Interview line:

> “I treat resource increase as the last option. First I fix skew and shuffle.”

---

# 3️⃣ Recovery strategy (important production piece)

If job failed mid-way:

* Ensure output is not partially corrupted:
  * write to temp path/table
  * commit only after success
* Make reruns safe:
  * idempotent writes (MERGE or overwrite partition)
  * dedupe logic if needed

---

# 4️⃣ Prevention (what I do so it doesn’t repeat)

* Add monitoring on:
  * shuffle size
  * spill to disk
  * GC time
  * skew (top key frequency)
* Add automated alerts when:
  * data volume spikes
  * partitions become too large
* Runbook: “OOM playbook”

---

# 5️⃣ Managerial / Communication Handling (simple English)

During incident:

> “Job failed due to executor memory pressure during heavy shuffle. No data loss. I’m applying partition + join optimizations and restarting.”

After fix:

> “Root cause: skew/shuffle/memory pressure. We added safeguards and monitoring to prevent recurrence.”

---

# ✅ How you relate it to NCCT / Glassbeam

> “In NCCT/Glassbeam-like batch pipelines, OOM usually happens on heavy join/groupBy days when data spikes or skew increases. I first check Spark UI for skew and shuffle, then fix via AQE/salting, broadcast joins, and partition tuning. Finally I make the job idempotent and add monitoring.”

---

## ✅ Q4: In Spark UI most tasks finish quickly but one task takes very long time. What does this indicate and how do you fix it?

### What this indicates (most important)

This pattern almost always means  **data skew** .

**Simple meaning:**
Spark splits data into partitions. If one partition has **too much data** (because one key is very common), then the executor handling that partition becomes a bottleneck. So 99% tasks finish, but **one “hot partition” task** keeps running.

---

# 1️⃣ Spark / Batch Debugging (Step-by-step)

## Step 1 — Confirm skew in Spark UI

Go to **Spark UI → Stages → the slow stage** and check:

* **Task time distribution**
  * One task takes 10x–100x longer
* **Input Size / Records per task**
  * That slow task typically has very high input size
* **Shuffle Read size**
  * Often, the skew shows up strongly in shuffle stages

✅ If one task has much higher input size than others → skew confirmed.

---

## Step 2 — Identify where skew is coming from

Skew usually happens in:

* **Join** (skewed join key like `customer_id`, `account_id`, `device_id`)
* **GroupBy** (one key has huge number of rows)
* **Repartition by key** (same skew issue)

To find the culprit key:

* Check which column is used in join/groupBy
* Run a quick “top keys” analysis (even on sampled data)

**Example idea (not exact code needed in interview):**

* count records by join key
* find top 10 keys

If one key dominates, that’s the hot key.

---

# 2️⃣ Fixes (Best options in interview order)

## ✅ Fix Option A: Enable AQE + Skew Join (fastest in Spark 3+)

This is the easiest production fix if available:

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
```

**What Spark does:**
It detects skewed partitions and automatically splits them into smaller chunks.

✅ Interview line:

> “If I’m on Spark 3+, AQE is my first switch because it handles skew joins automatically.”

---

## ✅ Fix Option B: Salting technique (best “senior” answer)

If AQE isn’t enough or not enabled, I use  **salting** .

### What is salting (simple explanation)

If one key is too frequent (example `customer_id=123`), then I add a small random number called **salt** so Spark treats it like multiple keys:

* `123_0`, `123_1`, `123_2` …
  Now data spreads across partitions.

### How it works in join

* Add salt column to the big table
* Duplicate/expand small table with same salt values
* Join on (key + salt)

✅ This converts **one heavy partition** into  **many balanced partitions** .

---

## ✅ Fix Option C: Change partition strategy

Sometimes repartitioning helps:

* repartition on a better key
* increase partitions

```python
df = df.repartition(600, "better_key")
```

But note: **repartition alone won’t fix skew** if the key itself is skewed. It only increases parallelism.

---

## ✅ Fix Option D: Handle skewed aggregations

If skew happens in `groupBy`:

* Do  **two-step aggregation** :
  1. partial aggregation with extra random prefix
  2. final aggregation

This spreads the heavy key load.

---

# 3️⃣ Production safety (important)

Skew often causes:

* SLA miss
* executor OOM

So after skew fix, I also verify:

* shuffle size reduced
* stage time stable
* no executor loss

---

# 4️⃣ Prevention (what I do so it doesn’t repeat)

* Add monitoring for:
  * top key frequency
  * stage time spikes
* Keep a list of known skewed keys in runbook
* Add AQE by default (if allowed)
* Add “skew handling” logic in code path for known hot keys

---

# 5️⃣ Managerial / communication handling

During incident:

> “Job is delayed because one partition is processing much more data (data skew). No data loss. I’m applying skew handling (AQE/salting) to balance the workload.”

After fix:

> “We added skew monitoring and mitigation so month-end/heavy days won’t delay the pipeline.”

---

# ✅ NCCT / Glassbeam-style line you can use

> “In my pipelines, some customers/devices can generate unusually high data, which creates skew. When I see one task running much longer in Spark UI, I treat it as skew and fix it using AQE or salting, plus monitoring for hot keys.”

---

## ✅ Q5: Spark job succeeded, but downstream tables contain duplicate records. How do you fix this and prevent it in future?

This is a **very important senior-level scenario** because the job “looks green” but the  **data is wrong** .

I handle it in  **4 clear parts** :

1. **Stop further damage**
2. **Identify why duplicates happened**
3. **Fix existing duplicates**
4. **Make the pipeline idempotent forever**

---

# 1️⃣ Immediate action — Stop further damage

First, I **pause downstream consumers** or reporting if possible, because wrong data is worse than no data.

Then I confirm:

* Which tables have duplicates
* From which date / batch the duplicates started
* Whether duplicates are **exact duplicates** or **same business key with multiple versions**

---

# 2️⃣ Identify the root cause (most common reasons)

From experience, duplicates in batch jobs usually come from one of these:

### A) Job was rerun without cleanup

* Previous data not deleted
* New data appended again

### B) Partial failure + rerun

* Job wrote some data
* Failed
* Reran → same data written again

### C) No unique key / idempotency logic

* Pure `insert` logic
* No merge or dedup step

### D) Late-arriving data mixed with reruns

* Same business key appears again with newer timestamp

I confirm this by:

* Checking job history / rerun logs
* Comparing record counts per run
* Checking load timestamps / batch IDs

---

# 3️⃣ Fix existing duplicates (technical correction)

## Step 1 — Identify duplicates using business key

Every table should have a **business key** (example: `order_id`, `customer_id + date`).

I find duplicates using window functions:

```sql
row_number() over (
  partition by business_key
  order by update_ts desc
)
```

* Keep `row_number = 1`
* Remove others

This ensures  **latest and correct record survives** .

---

## Step 2 — Reload corrected data safely

I reload data using:

* `MERGE` / `UPSERT` (preferred)
* or overwrite only affected partitions (not full table)

This avoids touching clean data.

---

# 4️⃣ Prevent duplicates forever (MOST IMPORTANT PART)

This is where you score big in interviews.

## ✅ Design batch jobs to be **idempotent**

**Meaning:**
If the same batch runs twice,  **output remains the same** .

### How I do this:

### A) Use MERGE instead of INSERT

* Match on business key
* Update if exists
* Insert if new

This makes reruns safe.

---

### B) Partition data by date / batch

* Each run writes to its own partition
* Rerun overwrites only that partition

Example mindset:

> “One date → one partition → overwrite is safe.”

---

### C) Deduplication step inside pipeline

Before writing:

* Deduplicate using business key + timestamp
* Keep latest record only

---

### D) Track batch metadata

* Add `batch_id`, `load_ts`
* Helps trace and safely clean reruns

---

# 5️⃣ Validation before publish (senior signal)

Before marking job as success:

* Check record counts
* Check duplicate count = 0
* Run basic data quality checks

If checks fail → job fails intentionally.

---

# 6️⃣ Managerial / communication handling

During incident:

> “Job completed but duplicate data was identified. We’ve paused downstream consumption and are correcting affected partitions. No permanent data loss.”

After fix:

> “Root cause was rerun without idempotency. We redesigned the job using merge-based loads and added validation to prevent duplicates.”

---

# ✅ NCCT / Glassbeam-style explanation you can say

> “In my batch pipelines, reruns are common. So I always design jobs to be idempotent using merge logic and deduplication on business keys. That way even if a job reruns, duplicates don’t happen.”

---

# ⭐ 30-second interview answer (short version)

> “Duplicates usually happen when a batch job reruns without idempotent logic. I first identify and clean duplicates using business keys and timestamps. Then I prevent it permanently by using merge-based loads, partition overwrite strategy, and validation checks so reruns are safe.”

---

## ✅ Q6: Upstream dependency ran late and your Spark batch job’s SLA is at risk. How do you handle this?

This is a  **very common real production + managerial question** .
Interviewers want to see  **technical flexibility + stakeholder communication** .

I handle this in  **4 clear steps** :

1. **Assess impact quickly**
2. **Apply technical workaround to protect SLA**
3. **Communicate clearly with business**
4. **Prevent this situation in future**

---

# 1️⃣ Immediate Assessment (first 5–10 minutes)

Before doing anything, I answer these questions:

* How late is the upstream job?
* Is data **completely missing** or  **partially available** ?
* Is downstream allowed to run with  **partial data** ?
* Is the SLA **hard** (dashboard cutoff) or  **soft** ?

This decides the strategy.

---

# 2️⃣ Spark / Batch Technical Handling

## ✅ Case A: Partial upstream data is available (most common)

### What I do

I  **do NOT block the entire pipeline** .

* Process **available partitions only**
* Skip missing partitions
* Mark missing data for later backfill

**How this looks in practice**

* Data partitioned by `date`
* If `2024-01-31` missing but `2024-01-30` present:
  * process available partitions
  * backfill missing one later

This keeps dashboards mostly fresh.

---

## ✅ Case B: Upstream is late but will finish soon (within SLA buffer)

### What I do

* Delay my job slightly (configurable wait)
* Use **sensor / polling logic** (Airflow/Glue)
* Avoid blind retries

This avoids unnecessary reruns.

---

## ✅ Case C: Upstream is very late / failed (cannot wait)

### What I do

I choose one of these (based on business agreement):

### Option 1: Run with last available data

* Use **previous day’s snapshot**
* Flag data as “partial / stale”

### Option 2: Run pipeline but exclude dependent metrics

* Produce rest of data
* Leave dependent fields null or default
* Backfill later

---

## ✅ Case D: SLA is more important than completeness

Some dashboards prefer **fresh but slightly incomplete** data.

In that case:

* Run Spark job with available data
* Clearly flag “partial data” downstream
* Schedule a backfill job once upstream completes

---

# 3️⃣ Make Spark job resilient (technical best practices)

To support late upstream data safely, I design batch jobs as:

### ✅ Incremental & partition-aware

* Process data by date/partition
* Overwrite or merge only affected partitions

### ✅ Idempotent

* Reruns or backfills won’t create duplicates
* Use MERGE or partition overwrite

### ✅ Backfill-friendly

* Accept date range as parameter
* Easy to rerun for specific dates

---

# 4️⃣ Communication (this is VERY important in interviews)

### During incident (early communication)

I inform stakeholders immediately:

> “Upstream job is delayed by X minutes. I’ll proceed with available data to meet SLA and backfill missing partitions once upstream completes. No data loss.”

This avoids surprises.

---

### After incident

* Share what happened
* Share what decision was taken (partial vs wait)
* Share when final corrected data will be available

---

# 5️⃣ Prevention (how I stop this happening again)

This is where you sound  **senior** .

### ✅ Decouple pipelines

* Avoid tight dependency on single upstream
* Use intermediate stable datasets

### ✅ SLA-aware orchestration

* Hard SLA → run with partial data
* Soft SLA → wait with timeout

### ✅ Monitoring & alerts

* Alert when upstream crosses threshold delay
* Alert when partitions are missing

### ✅ Clear data contracts

* Agree with business:
  * “Is partial data acceptable?”
  * “How late is too late?”

---

# ⭐ 30-second interview-ready summary

> “When an upstream job runs late, I first assess whether partial data is available and how strict the SLA is. If possible, I run with available partitions to protect SLA and backfill missing data later using idempotent logic. I communicate early with stakeholders and then add SLA-aware orchestration and monitoring to prevent repeat issues.”

---

## ✅ NCCT / Glassbeam-style line you can use

> “In my pipelines, upstream delays are common, so I design Spark jobs to be incremental and idempotent. That lets me meet SLA with partial data and safely backfill once upstream completes.”

---

## ✅ Q7: Business asks you to backfill last 30 days of data safely. How do you do it?

This is a  **very high-signal senior question** .
Interviewers want to see **safety, idempotency, isolation, and communication** — not just “rerun the job”.

I handle this in  **5 clear steps** .

---

# 1️⃣ First clarify scope (before touching data)

Before starting, I confirm:

* **Why** backfill is needed
  (data fix, late data, logic change?)
* **Exact date range** (last 30 days → from which date?)
* **Which tables** are impacted (raw, staging, curated?)
* **Is production data currently being consumed?**

This avoids accidental overwrites.

---

# 2️⃣ Design the backfill to be SAFE (most important)

## ✅ Key principles I follow

* **Never touch unaffected data**
* **Never block daily production loads**
* **Backfill must be rerunnable**
* **Backfill must be isolated**

---

## 3️⃣ Spark / Batch Technical Approach

### Step A — Parameterize the job by date

I make the Spark job accept:

* `start_date`
* `end_date`

So I can run:

```
2024-01-01 → 2024-01-30
```

without touching other dates.

---

### Step B — Process data partition by partition

Data is usually partitioned by date.

For each date:

* Read only that partition
* Transform data
* Write back only that partition

This limits blast radius.

---

### Step C — Use idempotent writes (critical)

Depending on table type:

### 🔹 For curated tables

* Use **MERGE** on business key
* Or overwrite only that date partition

This ensures:

* reruns don’t create duplicates
* partial failures are safe

### 🔹 For raw tables

* Usually append-only
* Backfill written to separate path if needed

---

### Step D — Control concurrency

I usually:

* Run backfill **in smaller batches** (e.g., 5 days at a time)
* Run during **off-peak hours**
* Avoid overlapping with daily production jobs

This prevents resource contention.

---

# 4️⃣ Validation after backfill (senior-level step)

For each date (or batch of dates), I validate:

* Record counts (before vs after)
* Duplicate count = 0
* Null / key checks
* Business metrics sanity check

If validation fails → stop backfill and fix.

---

# 5️⃣ Communication & coordination

### Before backfill

I inform stakeholders:

> “We’ll backfill last 30 days incrementally, without impacting today’s data. Final corrected data will be available by X.”

### During backfill

* Share progress updates
* Flag any unexpected issues early

### After backfill

* Share completion confirmation
* Mention validation checks passed

---

# 6️⃣ Prevention (so backfill is not frequently needed)

After completing backfill, I ask:

* Why did this happen?
* Can we handle this automatically next time?

Typical improvements:

* Better late-data handling
* Idempotent design everywhere
* Better data quality checks
* Clear rerun/backfill runbooks

---

# ⭐ 30-second interview answer (short & strong)

> “When asked to backfill data, I first isolate the date range, then run the Spark job in a parameterized and idempotent way — processing partition by partition using merge or partition overwrite. I validate each batch and ensure daily production jobs are not impacted. Finally, I communicate clearly and add safeguards to reduce future backfills.”

---

## ✅ NCCT / Glassbeam-style line you can use

> “In my pipelines, backfills are common, so all batch jobs are parameterized and idempotent. That allows me to safely reprocess historical dates without impacting live production.”

---






## ✅ Q8: Spark job succeeded, but business reports show incorrect numbers. How do you debug and handle it?

This is a **very senior scenario** because it tests whether you care about  **data correctness** , not just “job green”.

I handle it in a very structured way:

1. **Stop/limit impact**
2. **Find where the mismatch started**
3. **Prove root cause with data checks**
4. **Fix + backfill**
5. **Prevent permanently**

---

# 1️⃣ Immediate action: Protect business from wrong data

First I treat it as a  **data incident** .

* Identify which dashboards/reports are wrong
* Pause or flag the dataset if possible (so business doesn’t make decisions on wrong data)
* Inform stakeholders quickly:

> “Pipeline succeeded technically, but there’s a data mismatch. I’m investigating and will share ETA. We’ll avoid using incorrect numbers meanwhile.”

---

# 2️⃣ Narrow down the issue: where did it go wrong?

I do a **layer-by-layer trace** (this is key).

Typical layers:

* Raw / landing
* Staging
* Curated / marts
* Dashboard queries

✅ Goal: Find the first layer where numbers became incorrect.

### I compare:

* Yesterday vs today
* Source vs target
* Stage outputs vs final table

---

# 3️⃣ Debugging checklist (Technical — what I actually do)

## A) Check if input data itself changed

Even if code didn’t change, upstream data might have:

* Missing partitions
* Late data
* Schema change
* New values causing logic break

I check:

* row counts per date partition
* missing file/partition
* null spikes in key columns

---

## B) Reconcile counts at each step (most practical method)

I do quick reconciliations like:

* Source count vs landing count
* Landing vs staging count
* Staging vs curated count

If count drops or spikes at one stage → bug is in that stage.

✅ If counts match but business number differs → likely  **aggregation/join logic issue** .

---

## C) Check for duplicate data (very common)

“Wrong numbers” are often inflated due to duplicates.

I check:

* duplicate business keys
* rerun caused double insert
* missing idempotency

If duplicates exist → fix with dedupe + merge.

---

## D) Check join problems (most common logic issue)

Wrong numbers often happen due to:

* many-to-many join accidentally
* join key mismatch (trim/case/null)
* dimension table duplicates causing multiplication

How I confirm:

* Validate uniqueness of join keys in dimension table
* Compare counts before and after join
* Check if join increases rows unexpectedly

✅ Interview line:

> “If a join increases row count unexpectedly, I suspect join multiplicative issue.”

---

## E) Check filters and date logic (silent bugs)

Month-end / timezone / partition filters can cause:

* missing day
* extra day
* wrong timezone conversion

I verify:

* event date vs processing date
* partition selection logic
* inclusive/exclusive date boundaries

---

## F) Check schema/type issues (silent wrong results)

Example:

* numeric stored as string
* cast failures leading to nulls
* decimal precision issues

I validate:

* data types
* null count after casts
* rounding/precision

---

# 4️⃣ Fix and recovery (corrective steps)

Once root cause is confirmed:

## ✅ If it’s duplicates

* Deduplicate by business key + latest timestamp
* Reload affected partitions
* Add idempotent merge

## ✅ If it’s join multiplication

* Fix by enforcing uniqueness in dim table
* Use correct join keys
* Deduplicate dimension before join
* Recompute affected partitions

## ✅ If it’s missing/late data

* Backfill missing partitions
* Update watermark logic in batch (incremental loads)

### Important: fix only affected dates

I don’t reload everything unless needed. I backfill only impacted partitions (safe + fast).

---

# 5️⃣ Communication (managerial part)

This is very important.

### During incident

> “Job succeeded but data validation failed at metric X. We are investigating root cause. ETA for correction: X. We will backfill and re-publish.”

### After fix (RCA)

I share:

* what went wrong (root cause)
* what was the impact (which reports/dates)
* what we fixed (code + backfill)
* what we’ll add to prevent recurrence

---

# 6️⃣ Prevention (how I ensure it never repeats)

This part makes you sound senior.

✅ Add “data quality gates” before marking job success:

* row count checks vs historical baseline
* duplicate count must be zero
* join sanity checks (row count shouldn’t explode)
* null thresholds
* business metric reconciliation checks

If these fail → pipeline should fail intentionally and alert.

✅ Add monitoring:

* data drift alerts
* missing partition alerts
* schema evolution detection

---

# ⭐ 30-second interview-ready summary

> “If business numbers are wrong even though Spark job succeeded, I treat it as a data incident. I trace the issue layer-by-layer using reconciliation checks to find where the mismatch starts. Common root causes are duplicates, join multiplication, missing partitions, or casting issues. Once identified, I fix logic and backfill only affected partitions. Finally I add data-quality gates and monitoring so the job cannot be marked successful when data is wrong.”

---

## ✅ NCCT/Glassbeam-style line

> “In my pipelines, I don’t trust ‘job success’ alone. I always validate business-critical metrics and add automated checks so incorrect numbers are caught before dashboards consume them.”

---
