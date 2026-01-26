Below are **complete, memory-friendly IAM notes with Amazon interview questions**, written **exactly like S3** so you can revise fast and answer confidently.

---

# 🔐 AWS IAM (Identity and Access Management) — Complete Notes + Interview Q&A

Amazon Web Services

![Image](https://docs.aws.amazon.com/images/IAM/latest/UserGuide/images/intro-diagram%20_policies_800.png)

![Image](https://d2908q01vomqb2.cloudfront.net/cb4e5208b4cd87268b208e49452ed6e89a68e0b8/2022/02/11/IAM-Users-vs-IAM-Roles-1.png)

![Image](https://d2908q01vomqb2.cloudfront.net/22d200f8670dbdb3e253a90eee5098477c95c23d/2024/07/05/img3-1.png)

---

## 1️⃣ What is IAM?

**AWS IAM** controls **who can access what in AWS and how**.

IAM answers **three questions**:

1. **Who** → User / Role
2. **What** → Resource (S3, Glue, Lambda…)
3. **How** → Policy (Allow / Deny)

### Interview one-liner

> *“IAM is used to securely control access to AWS resources using users, roles, and policies, following least-privilege principles.”*

---

## 2️⃣ Core IAM Components (MUST KNOW)

### 🔹 IAM User

* Represents a **human or application**
* Has long-term credentials (password / access key)

⚠️ **Avoid users for services**

---

### 🔹 IAM Role (VERY IMPORTANT ⭐)

* Used by **AWS services**
* No long-term credentials
* Temporary credentials via **assume role**

Examples:

* Glue role → access S3
* Lambda role → trigger Glue
* EMR role → read/write S3

Amazon LOVES this line:

> **“AWS services should always use IAM roles, not access keys.”**

---

### 🔹 IAM Policy

* JSON document defining permissions
* Attached to users / roles / groups

Basic structure:

* Effect (Allow / Deny)
* Action (s3:GetObject)
* Resource (bucket / object)

---

### 🔹 IAM Group

* Collection of users
* Simplifies permission management

---

## 3️⃣ IAM in Data Engineering (REAL usage)

| Service  | IAM Role Purpose             |
| -------- | ---------------------------- |
| S3       | Read / write data            |
| Glue     | Read raw data, write curated |
| Lambda   | Trigger jobs, DQ checks      |
| EMR      | Access S3 + logs             |
| Athena   | Read metadata + S3           |
| Redshift | Spectrum access to S3        |

Interview line:

> *“Each AWS service has a dedicated IAM role with minimum required permissions.”*

---

## 4️⃣ IAM Policies (Key Concepts)

### Types of Policies

1. **AWS Managed** – Predefined by AWS
2. **Customer Managed** – Created by you (preferred)
3. **Inline** – Embedded (avoid)

### Least Privilege Principle ⭐

* Grant **only required actions**
* Avoid `s3:*` or `*:*`

Bad ❌

```json
"Action": "*",
"Resource": "*"
```

Good ✅

```json
"Action": "s3:GetObject",
"Resource": "arn:aws:s3:::bucket-name/*"
```

---

## 5️⃣ IAM Role vs IAM User (VERY COMMON QUESTION)

| Feature         | User      | Role         |
| --------------- | --------- | ------------ |
| Credentials     | Long-term | Temporary    |
| Used by         | Humans    | AWS services |
| Rotation needed | Yes       | No           |
| Best practice   | Limited   | Preferred    |

Perfect answer:

> *“Users are for humans, roles are for services.”*

---

## 6️⃣ Security Best Practices (Amazon cares a LOT)

✅ Use IAM roles
✅ Enforce least privilege
✅ No hardcoded credentials
✅ Enable MFA for users
✅ Rotate access keys
✅ Use separate roles per service
✅ Audit via CloudTrail

---

## 7️⃣ Common IAM Mistakes (Mention in interviews)

❌ Hardcoding access keys
❌ Using root account
❌ Over-permissioned roles
❌ Sharing credentials
❌ One role for everything

---

## 8️⃣ IAM & S3 (Very common follow-up)

### How does Glue access S3?

> Glue **assumes an IAM role** that has S3 permissions.

### What controls access?

* IAM role policy
* S3 bucket policy (optional)

Golden line:

> *“Access is granted only if both IAM and resource policies allow it.”*

---

## 9️⃣ AWS IAM Interview Questions & Answers (Amazon-style)

### Q1. What is IAM?

> IAM manages authentication and authorization for AWS resources.

---

### Q2. Role vs User?

> Users are for humans, roles are for AWS services with temporary credentials.

---

### Q3. What is least privilege?

> Granting only the minimum permissions required to perform a task.

---

### Q4. How do AWS services authenticate?

> By assuming IAM roles.

---

### Q5. Can IAM restrict access to specific S3 paths?

> Yes, using resource-level permissions.

---

### Q6. What happens if IAM allows but bucket policy denies?

> ❌ Access denied — explicit deny always wins.

---

### Q7. How do you avoid credential leaks?

> Use IAM roles, avoid access keys, enable MFA.

---

## 🔟 BAR RAISER STAR SUMMARY (MEMORIZE)

> *“I secured AWS data pipelines by using IAM roles for all services, enforcing least-privilege policies, avoiding hardcoded credentials, and auditing access using CloudTrail.”*

---

## 🧠 FINAL MEMORY HOOK

> **IAM = Who + What + How**
> **Users → Humans**
> **Roles → Services**

---


