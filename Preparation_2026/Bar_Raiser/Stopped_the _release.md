# SITUATION 1 :

## Stopped the Release due to Bad Data

### Questions :

* Tell me about a time when you  **stopped or delayed a release because the data wasn’t correct** .
* Tell me about a time when  **everything looked fine at a high level** , but you still found a serious data issue.
* Describe a situation where  **technical checks passed** , but the data was still  **incomplete or wrong** .
* Tell me about a time when you  **identified a data issue by analyzing patterns or distributions** .
* Tell me about a **challenging data quality issue** you handled under deadline pressure.

### STAR :

#### **Situation**

I was working on the **NCCT annual cost submission pipeline** that prepares healthcare claims data for  **BCBSA** .
The pipeline completed successfully, all technical checks were green, and overall aggregates were within expected ranges.

However, during final validation, I noticed that although totals looked normal, the **distribution of claims across provider segments had shifted** compared to previous submission cycles.

---

#### **Task**

As the  **owner of the pipeline** , my responsibility was to ensure the data was  **business-correct** , not just technically successful, especially since this data directly impacts consumer cost estimates and is part of a regulatory submission.

---

#### **Action**

I **paused the release** and **dived deep** into the data:

* Broke the data down by **provider type and service category**
* Compared current distributions with **previous NCCT submissions and claims history**
* Identified that  **claim lines for one active provider segment were completely missing for a continuous 30-day period** , even though the values present were accurate

Given historical patterns, it’s statistically unrealistic for an active provider segment to have  **zero claims for an entire month** , which indicated a logical data gap rather than a business anomaly.

I then  **reached out to the upstream team** , shared the specific gap I observed — including the affected provider types and date range — and asked them to independently verify it.
Through follow-up analysis, we confirmed that a  **configuration change introduced during one of their releases unintentionally filtered out a subset of providers** . This was later corrected in their subsequent release, which explained the  **30-day gap in the middle** .

I  **discussed the risk early with my manager** , clearly explaining that although the pipeline had technically succeeded, releasing the data would lead to incorrect cost representation.

To resolve and prevent recurrence, I:

* Coordinated with the upstream team to **regenerate corrected data** for the impacted date range
* Validated the backfilled data using **provider-level distribution checks**
* Enhanced our **Lambda-based DQ framework** to include **historical variance and provider-level completeness validations**
* Communicated a **slightly adjusted but safe timeline** to stakeholders

---

#### **Result**

* Prevented **incomplete cost data** from being submitted to BCBSA
* The release was delayed by **less than one day**
* The new business-level validations became a **permanent standard** for future NCCT submissions
* Improved stakeholder trust by prioritizing **data accuracy over speed**

---

#### **Learning**

This experience reinforced that  **technical success does not guarantee business correctness** .
I learned to always validate data at multiple grains and to treat **missing data** as seriously as incorrect data. Since then, I design pipelines with  **business-level guardrails built in by default** , so these issues are caught automatically rather than relying on manual discovery.

---

#### **30-Second Verbal Summary (Optional)**

> Everything looked correct at a high level, but a provider segment having zero claims for 30 days was unrealistic. I stopped the release, worked with the upstream team to fix the extraction gap, backfilled the data, and raised our data quality standard permanently.

---

#### PRINCIPLES COVERED

| Leadership Principle | Likely Question                |
| -------------------- | ------------------------------ |
| Highest Standards    | Stopped/delayed due to quality |
| Dive Deep            | Hidden issue found via data    |
| Ownership            | Owned end-to-end correctness   |
| Backbone             | Pushed back under pressure     |
| Are Right, A Lot     | Judgment validated             |
| Earn Trust           | Transparent communication      |
