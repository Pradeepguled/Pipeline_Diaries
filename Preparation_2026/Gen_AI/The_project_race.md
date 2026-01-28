
---

# 🔍 Tracing the Project Input Step by Step

We’ll follow **one HL7 log file** from start to finish.

---

## 🔹 STEP 0: Raw Input (Starting Point)

### Input

A raw HL7 log file stored in S3.

**File:**

```
s3://hl7-logs/deviceA_20260118.log
```

**Content (raw):**

```
MSH|^~\&|LAB|HOSP|EHR|HOSP|202601180930||ORU^R01|MSG0001|P|2.3
PID|1||123456^^^||JOHN^DOE||19900101|M|||12 MAIN ST^^BLR||9876543210
OBR|1||...
OBX|1|...

ERROR: ACK not received

MSH|^~\&|LAB|HOSP|EHR|HOSP|202601180935||ORU^R01|MSG0002|P|2.3
PID|1||789012^^^||ANU^K||19950302|F|||45 PARK ST^^BLR||9988776655
OBR|1||...
OBX|1|...
```

---

## 🔹 STEP 1: Ingestion (S3 → Pipeline)

### Input

* S3 file key
* ETag / LastModified

### What happens

* Pipeline checks: **Is this file new or updated?**
* If yes → process
* If no → skip

### Output

Raw text loaded into memory.

✅ **Still unchanged content**

---

## 🔹 STEP 2: Chunking (HL7-aware)

### Input

Full log text (large)

### What happens

* Split text whenever a line starts with `MSH|`
* Each HL7 message becomes **one chunk**

### Output (Chunks)

**Chunk 1**

```
MSH|...|ORU^R01|MSG0001|...
PID|...JOHN^DOE...
OBR|...
OBX|...
ERROR: ACK not received
```

**Chunk 2**

```
MSH|...|ORU^R01|MSG0002|...
PID|...ANU^K...
OBR|...
OBX|...
```

👉 Now we have **2 independent chunks**

---

## 🔹 STEP 3: PHI Masking

### Input

Each HL7 chunk (with patient data)

### What happens

* Find `PID|` segment
* Replace sensitive fields:

  * Name
  * MRN
  * DOB
  * Address
  * Phone

### Output (Masked Chunk 1)

```
MSH|...|ORU^R01|MSG0001|...
PID|1||ID_REDACTED^^^||NAME_REDACTED||DOB_REDACTED|M|||ADDRESS_REDACTED||PHONE_REDACTED
OBR|...
OBX|...
ERROR: ACK not received
```

👉 **Meaning is preserved, identity removed**

---

## 🔹 STEP 4: Metadata Extraction

### Input

Masked HL7 chunk

### What happens

From `MSH` segment, extract:

* Message type → `ORU^R01`
* Message ID → `MSG0001`
* Timestamp → `202601180930`
* Source file → `deviceA_20260118.log`

### Output (Metadata)

```json
{
  "message_type": "ORU^R01",
  "message_id": "MSG0001",
  "timestamp": "202601180930",
  "source_file": "deviceA_20260118.log"
}
```

---

## 🔹 STEP 5: Embeddings (OpenAI)

### Input

Masked HL7 chunk text (plain text)

### What happens

* Text is sent to OpenAI embeddings API
* API converts text → numbers

### Output

Embedding vector:

```
[0.021, -0.334, 0.812, ...]
```

👉 This vector represents the **meaning** of the HL7 message.

---

## 🔹 STEP 6: Vector Storage (Chroma)

### Input

* Embedding vector
* Masked HL7 text
* Metadata

### What happens

* Stored as one record in Chroma

### Stored record (conceptually)

```json
{
  "id": "deviceA#MSG0001",
  "document": "<masked HL7 message>",
  "embedding": [0.021, -0.334, 0.812],
  "metadata": {
    "message_type": "ORU^R01",
    "timestamp": "202601180930",
    "source_file": "deviceA_20260118.log"
  }
}
```

👉 Repeat for every HL7 message.

---

# 🔎 QUERY SIDE (How Search Works)

---

## 🔹 STEP 7: User Query

### Input

User types:

```
"ACK missing for ORU messages"
```

---

## 🔹 STEP 8: Query Embedding

### Input

User query text

### Output

Query embedding:

```
[0.019, -0.301, 0.799, ...]
```

---

## 🔹 STEP 9: Semantic Search (Chroma)

### Input

* Query embedding
* Vector database

### What happens

* Chroma compares query vector with stored vectors
* Finds closest matches (Top-K)

### Output

Top result:

* Chunk with `ERROR: ACK not received`
* Message ID: `MSG0001`

---

## 🔹 STEP 10: (Optional) RAG Explanation

### Input

Retrieved HL7 chunks

### Output (Human-friendly answer)

> “ACK was not received for ORU^R01 message MSG0001 at 09:30. This usually indicates a receiver or network issue.”

---

# 🧠 Final One-Line Summary

> Raw HL7 logs are split into messages, masked for PHI, converted into embeddings, stored in a vector database, and later retrieved semantically to answer user queries.

---

## 🎯 Interview Tip

If you explain it like this — **input → output → input → output** — interviewers will instantly trust your understanding.
