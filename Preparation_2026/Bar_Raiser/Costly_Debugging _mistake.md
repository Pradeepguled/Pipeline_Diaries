---

# STORY 2 – Owning a Costly Debugging Mistake and Fixing It

## Leadership Principles Covered

Ownership
Bias for Action
Frugality
Dive Deep
Deliver Results
Learn and Be Curious

---

## ⭐ Question Variants This Answers

* Tell me about a failure you owned
* Tell me about a time you made a mistake
* Tell me about something that went wrong in production
* Tell me about balancing speed and cost
* Tell me about a tough situation

---

## ✅ Situation

I was working on an AWS-based batch data pipeline built using **S3, Glue (Spark), Lambda, Step Functions, and Snowflake**.

A critical Glue job started failing in production, which blocked downstream Snowflake loads and delayed analytics reports tied to business SLAs.

To safely debug the issue without affecting production, I decided to reproduce the failure in the UAT environment.

UAT was intentionally configured with lower DPUs and executor memory to control cost.

---

## ✅ Decision & Mistake

To eliminate environment differences and reproduce the issue accurately, I increased UAT Glue configuration to match production DPUs and memory settings.

My assumption was that reproducing the issue under identical conditions would help isolate the root cause quickly.

However, I underestimated:

* The number of retries required during debugging
* The cumulative cost impact of running multiple high-DPU jobs
* How Spark retries and wide transformations amplify compute usage

Within a short time window, UAT Glue costs increased approximately 3–4x the normal daily average.

The decision to scale UAT resources was mine.

---

## ✅ Immediate Action (Bias for Action)

As soon as I noticed the cost spike:

* I stopped further high-configuration runs immediately
* Reviewed CloudWatch metrics and Spark execution plans
* Analyzed executor memory and shuffle behavior
* Compared dataset size and processing patterns

I realized infrastructure scaling was masking the real issue rather than solving it.

---

## ✅ Root Cause

The actual problem was not memory or DPUs.

The root cause was:

* Full historical dataset being reprocessed instead of incremental partitions
* Inefficient join strategy causing wide shuffles
* No retry cap configured in Step Functions for UAT
* Lack of cost guardrails in lower environments

The issue was architectural, not infrastructural.

---

## ✅ Long-Term Mechanism (Most Important for L5)

I implemented:

1. Incremental partition-based processing logic
2. Optimized join strategy to reduce shuffle
3. Reduced UAT DPU ceiling to prevent uncontrolled scaling
4. Added retry limits in Step Functions for non-production environments
5. Created CloudWatch cost anomaly alerts for Glue jobs
6. Introduced a lightweight design checklist requiring cost impact review before infrastructure scaling

This turned a one-time mistake into a systemic improvement.

---

## ✅ Result

* Production issue was identified and fixed
* SLA compliance was restored
* UAT Glue cost returned to normal range
* No similar cost spikes occurred afterward
* Team adopted cost-awareness practice in debugging workflows

---

## ✅ Reflection

This experience fundamentally changed how I approach debugging in cloud environments.

Earlier, my priority was reproducing failures quickly.
Now I explicitly evaluate second-order effects such as cost, retries, and scaling behavior before changing infrastructure configurations.

I learned to treat cost as a first-class engineering metric alongside reliability and performance.

---

## 🎯 One-Line Summary

> I scaled UAT infrastructure to reproduce a production failure, underestimated retry-driven cost impact, owned the mistake immediately, fixed the architectural issue, and implemented guardrails to prevent similar cost spikes in the future.

---