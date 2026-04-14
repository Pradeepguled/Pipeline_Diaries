🔥 STORY 3 – Owning a Costly Debugging Mistake
✅ Question It Answers

Tell me about a failure.

Tell me about a mistake you made.

Tell me about something that went wrong.

Tell me about a time you balanced speed and cost.

Tell me about ownership.

⭐ Situation

I was working on an AWS batch data pipeline using S3, Glue, Lambda, Step Functions, and Snowflake.

One of our Glue jobs started failing in production.
Because of this, downstream reports were delayed and it was impacting business SLAs.

To debug safely, I tried to reproduce the issue in the UAT environment.

UAT normally runs with lower compute to control cost.

⭐ Decision (My Mistake)

To reproduce the issue exactly like production, I increased the Glue DPUs and memory in UAT to match production settings.

My intention was to find the root cause faster.

However, I underestimated:

How many times I would re-run the job

How Spark retries increase compute usage

How wide joins increase shuffle cost

The total cost impact of multiple high-DPU runs

Because of repeated debugging runs, UAT cost increased to about 3–4 times the normal daily average.

This decision was mine.

⭐ Immediate Action

As soon as I noticed the cost spike:

I stopped running the high-DPU jobs immediately

I checked CloudWatch metrics

I reviewed Spark execution plans

I analyzed memory usage and shuffle behavior

I realized increasing infrastructure was not solving the real problem.

⭐ Root Cause

The real issue was not memory.

It was:

The job was reprocessing full historical data instead of incremental partitions

Inefficient joins were causing heavy shuffles

No retry limit was configured in UAT Step Functions

So the problem was architectural, not infrastructure size.

⭐ What I Did to Fix It (Long-Term Mechanism)

I implemented:

Incremental partition-based processing

Optimized join strategy

Retry limits in UAT Step Functions

Reduced maximum allowed DPUs in UAT

Added cost anomaly alerts for Glue jobs

Created a small checklist to evaluate cost impact before scaling infrastructure

⭐ Result

Production issue was fixed

SLA was restored

UAT costs returned to normal

No similar cost spikes happened again

Team became more cost-aware during debugging

⭐ Learning

Earlier, I focused only on fixing issues quickly.

Now I always think about:

Cost impact

Retry behavior

Second-level effects of scaling

I learned that cost is also an engineering responsibility, not just performance.

⭐ One-Line Summary

I increased UAT compute to debug a production issue, underestimated retry-driven cost impact, owned the mistake immediately, fixed the real architectural issue, and added guardrails to prevent similar cost spikes.

This version is:

Clear

Honest

Strong

Easy to say under pressure

Defensible

Now answer this in simple English:

If the interviewer asks:

“Why didn’t you think about cost before increasing DPUs?”

What will you say?