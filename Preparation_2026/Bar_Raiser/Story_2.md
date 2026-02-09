
# STORY : 2

## Owning a Costly Debugging Mistake and Fixing It

### Questions :

* Tell me about a **tough situation** you faced at work.
* Tell me about a  **failure you owned** .
* Tell me about a time when you **made a mistake** and corrected it.
* Tell me about a time when something  **went wrong in production** .
* Tell me about a time when you had to  **balance speed and cost** .

---

## **STAR + Learning: Tough Situation / Failure I Owned (Cloud Cost Issue)**

### **Situation**

I was working on an AWS batch data pipeline using **S3, Glue (Spark), Lambda, Step Functions, and Snowflake**.

A Glue job **started failing in production**. To understand the issue properly, I tried to **reproduce the same failure in the UAT environment**.
UAT was **intentionally configured with lower resources than production** to control cost.

---

### **Task**

I was responsible for:

* Reproducing the production issue safely
* Finding the root cause quickly
* Avoiding further impact on production
* Making decisions under time pressure while keeping cost in mind

---

### **Action**

To remove environment differences, I compared UAT and production configurations. Since production had **higher DPUs and executor memory**, I increased the **UAT configuration to match production**.

This helped me reproduce the production behavior. However, I **underestimated two things**:

* How many times the job would need to be retried during debugging
* How much cost would increase when running **multiple retries with production-level resources**

Because of this, the Glue job ran several times in UAT with higher configuration, and **Glue costs increased multiple times within a short period**.

Once I noticed the cost spike, I stopped further retries and took ownership of the issue.
I then:

* Checked Spark metrics and saw that **memory was not the real problem**
* Identified that the actual issue was **inefficient logic and repeated data processing**
* Reduced the UAT configuration back to a **lower, cost-controlled setup**
* Optimized the job to process **only incremental data**
* Added guards to **limit retries** in UAT
* Tested fixes using **smaller datasets** instead of full runs

---

### **Result**

* The production issue was identified and fixed
* The pipeline stabilized and met SLAs
* Glue costs stopped increasing and returned close to normal
* No further unexpected bills occurred
* The same issue did not repeat

---

### **Learning**

This was a strong learning experience for me.

I learned that:

* Matching UAT to production can help debugging, but must be done **carefully**
* Multiple retries with high configuration can **quickly increase cloud cost**
* Cost should be treated as a **first-class concern**, even in non-production environments

Since then, I:

* Set **retry limits** in lower environments
* Use **sampled data** for debugging
* Always estimate **cost impact** before changing configurations

---

### **One-Line Summary**

> I matched UAT to production to debug a failure, but underestimated the cost impact of multiple retries — I owned the mistake and fixed both the logic and the process.

---
