
Spark can execute **40 tasks in parallel**.

---

### 23.4 Common Cluster Misconfigurations (Interview Traps)

❌ Too many executors with 1 core  
❌ Blindly increasing memory without fixing skew  
❌ Using default shuffle partitions for all jobs  
❌ Very large executors causing GC pauses  

**Interview-safe line:**  
I first fix shuffle and skew issues before increasing memory.

---

## 24. Situation-Based Spark Interview Questions (MOST IMPORTANT)

These questions test **real production understanding**, not theory.

---

### Q1. “Your Spark job is very slow. How do you debug it?”

**Expected approach:**
1. Open Spark UI
2. Identify slow stages
3. Check shuffle read/write
4. Look for skew (task duration imbalance)
5. Inspect join strategy
6. Optimize partitions or joins

**Interview-ready answer:**  
I use Spark UI to identify shuffle-heavy stages and skew, then optimize joins or partitioning.

---

### Q2. “Your job is stuck at 99%. What could be the reason?”

**Correct reasons:**
- Data skew
- One task processing a huge partition
- Single executor overloaded

**Interview-ready answer:**  
Jobs stuck at 99% usually indicate skew where one task is doing most of the work.

---

### Q3. “Spark job is failing with OutOfMemory error. What do you do?”

**Correct steps:**
- Identify whether OOM is at driver or executor
- Check shuffle-heavy stages
- Reduce partition size
- Fix skew
- Avoid collect()
- Use broadcast joins if possible

❌ Wrong answer: Just increase memory

**Interview-ready answer:**  
I fix shuffle and skew first and treat memory increase as the last option.

---

### Q4. “How do you optimize a join between two large tables?”

**Expected steps:**
- Check if one table can be broadcast
- Repartition by join key
- Handle skew
- Use bucketing if joins are repeated

**Interview-ready answer:**  
I optimize joins by minimizing shuffle using broadcast joins, repartitioning, or bucketing.

---

### Q5. “You see too many small files in S3. How do you fix it?”

**Correct fixes:**
- Use coalesce before write
- File compaction
- Reduce output partitions

**Interview-ready answer:**  
I use coalesce before writing to avoid the small file problem and reduce metadata overhead.

---

### Q6. “When should you NOT cache a DataFrame?”

**Correct reasons:**
- Used only once
- Very large dataset
- Memory constrained cluster

**Interview-ready answer:**  
Caching is useful only when data is reused multiple times.

---

### Q7. “How do you handle skewed joins?”

**Correct techniques:**
- Broadcast join
- Salting
- AQE
- Separate heavy keys

**Interview-ready answer:**  
I identify skew using Spark UI and apply broadcast or salting depending on data size.

---

### Q8. “What happens if an executor fails?”

**Correct behavior:**
- Tasks running on that executor fail
- Spark recomputes lost partitions using lineage
- Job continues

**Interview-ready answer:**  
Spark provides fault tolerance using immutable RDDs and lineage.

---

### Q9. “Why repartition before join?”

**Correct reasons:**
- Balance data distribution
- Reduce skew
- Improve parallelism

---

### Q10. “Why not always use broadcast joins?”

**Correct reasons:**
- Broadcast table too large
- Risk of executor OOM
- Memory constraints

**Interview-ready answer:**  
Broadcast joins are effective only when the dataset is small enough to fit in executor memory.

---

## 25. Most Important Interview Pattern (REMEMBER)

Interviewers listen for:
- Spark UI
- Shuffle
- Skew
- Trade-offs

Mentioning these shows **real production experience**.

---

## FINAL INTERVIEW GOLDEN SUMMARY

Spark performance issues usually arise from shuffle, skew, or poor partitioning. I debug issues using Spark UI, minimize shuffle using broadcast joins and repartitioning, and tune cluster configurations based on workload characteristics.
