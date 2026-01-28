
---

## Project Explanation (Final Interview Version)

### Problem

We had a large volume of **HL7 healthcare logs** stored in S3.
Searching these logs using keywords was slow and often inaccurate, especially for issues like ACK failures or ORU message errors.
We also had to make sure **patient data was protected**, which limited how AI could be used.

---

### Solution

I built an **end-to-end semantic search pipeline** that allows HL7 logs to be searched by meaning instead of keywords, while remaining PHI-safe.

---

### Architecture & Flow

1. **Ingestion**
   HL7 logs are read from S3. New or updated files are detected using ETag or last modified time.

2. **Chunking**
   Each HL7 message is treated as one chunk using the MSH segment as the boundary.

3. **PHI Masking**
   Sensitive patient identifiers in PID fields are replaced with safe placeholders before any AI processing.

4. **Embeddings**
   Each masked HL7 message is converted into an embedding using OpenAI.

5. **Vector Storage**
   Embeddings, log text, and metadata are stored in **Chroma**, enabling semantic search.

6. **Search & RAG (Optional)**
   User queries are embedded and matched against stored vectors. The most relevant HL7 messages are retrieved and optionally passed to an LLM using RAG to generate clear, context-based explanations.

---

### My Role

This was an **end-to-end ownership project**.
I designed the architecture and implemented the complete pipeline myself, focusing on data engineering reliability and safe AI integration.

---

### Business Impact

* Faster troubleshooting of HL7 issues
* Reduced manual log scanning
* Improved accuracy compared to keyword search
* Safe adoption of AI in a healthcare environment

---

### 30-Second Summary (Very Important)

> I built a semantic search pipeline for HL7 logs stored in S3. Logs are chunked by HL7 message boundaries, PHI is masked, embeddings are generated, and everything is stored in Chroma for semantic search. This allows engineers to search logs by meaning instead of keywords, and optionally get AI-generated explanations using RAG. The solution significantly improved troubleshooting speed while maintaining healthcare compliance.

---


