---
# 📘 DATA MODELLING — COMPLETE NOTES

*(Using our Dimensional / Star Schema Example)*
---
## 1️⃣ What is Data Modelling? (Simple Definition)

**Data modelling** is the process of **structuring data** so that:

* It is easy to **store**
* Easy to **query**
* Fast to **analyze**
* Reliable and **consistent**

👉 In analytics systems, **data modelling is more important than writing SQL**.

---

## 2️⃣ Types of Data Models (Interview MUST)

### 1. Conceptual Model

* High-level view
* No tables, no columns
* Only **business entities**
* Example: Customer, Order, Product

📌 Used by business stakeholders

---

### 2. Logical Model

* Defines **tables & relationships**
* Still no DB-specific details
* Example: Customer → Orders → Order Items

📌 Used by architects

---

### 3. Physical Model

* Actual **CREATE TABLE**
* Data types, keys, indexes
* Optimized for performance

📌 Used by data engineers (YOU)

---

## 3️⃣ OLTP vs OLAP (Very Important)

| Feature | OLTP         | OLAP                 |
| ------- | ------------ | -------------------- |
| Usage   | Transactions | Analytics            |
| Inserts | Frequent     | Batch                |
| Updates | Frequent     | Rare                 |
| Joins   | Few          | Many                 |
| Schema  | Normalized   | Denormalized         |
| Example | MySQL app DB | Snowflake / Redshift |

👉 **Dimensional modelling is for OLAP**

---

## 4️⃣ Why Dimensional Modelling?

Interview one-liner 👇

> *Dimensional modelling is used to make analytical queries fast, simple, and business-friendly.*

### Problems with normalized models for analytics:

* Too many joins
* Slow queries
* Hard to understand

### Dimensional model solves this by:

* Fewer joins
* Predictable query patterns
* Faster aggregations

---

## 5️⃣ Core Concepts in Dimensional Modelling

### 🔹 Fact Tables

* Store **measures**
* Numeric, additive
* Very large (millions/billions of rows)

Examples:

* `fact_sales`
* `fact_sales_item`

Measures:

* `total_amount`
* `qty`
* `line_amount`

---

### 🔹 Dimension Tables

* Store **descriptive attributes**
* Used for filtering, grouping, reporting

Examples:

* `dim_customer`
* `dim_product`
* `dim_date`
* `dim_employee`

Attributes:

* name, city, category, date, department

---

## 6️⃣ Grain (🔥 MOST IMPORTANT INTERVIEW CONCEPT)

**Grain = what one row represents**

### Examples from our model:

| Table               | Grain                         |
| ------------------- | ----------------------------- |
| `fact_sales`      | One row per order             |
| `fact_sales_item` | One row per order per product |
| `dim_customer`    | One row per customer          |
| `dim_date`        | One row per date              |

📌 **Rule**:

> Always define grain BEFORE designing columns

---

## 7️⃣ Star Schema (Our Example)

### Structure

```
           dim_date
              |
dim_customer — fact_sales — (degenerate order_id)
              |
         dim_product (via fact_sales_item)
```

### Why Star Schema?

* Simple joins
* Best performance
* Easy for BI tools

---

## 8️⃣ Snowflake Schema (Interview Comparison)

| Star Schema       | Snowflake Schema |
| ----------------- | ---------------- |
| Denormalized dims | Normalized dims  |
| Faster queries    | More joins       |
| Simple            | Complex          |
| Preferred         | Rare             |

👉 **Always say**:

> We prefer star schema unless storage is a constraint

---

## 9️⃣ Surrogate Key vs Business Key

### Business Key

* Comes from source system
* Example: `customer_id`, `emp_id`

### Surrogate Key

* Generated internally
* Example: `customer_key`, `employee_key`

📌 **Why surrogate keys?**

* Stable
* Supports Slowly Changing Dimensions
* Faster joins

👉 In our model:

```text
customer_id  → business key
customer_key → surrogate key
```

---

## 🔟 Fact Table Types (Interview Favorite)

### 1. Transaction Fact

* One row per event
* Example: `fact_sales_item`

### 2. Periodic Snapshot Fact

* One row per period
* Example: daily revenue table

### 3. Accumulating Snapshot Fact

* Tracks lifecycle
* Example: order placed → shipped → delivered

📌 Our `fact_sales` is a **transaction fact**

---

## 1️⃣1️⃣ Additive, Semi-additive, Non-additive Measures

| Measure              | Type          |
| -------------------- | ------------- |
| Sales Amount         | Additive      |
| Quantity             | Additive      |
| Account Balance      | Semi-additive |
| Ratios / Percentages | Non-additive  |

👉 Always mention this in interviews

---

## 1️⃣2️⃣ Degenerate Dimension

A dimension attribute stored **inside fact table**.

Example:

```sql
fact_sales.order_id
```

* No separate dimension table
* Still useful for filtering

📌 Interview gold term

---

## 1️⃣3️⃣ Date Dimension (Why Not Use DATE?)

Reasons:

* Easy filtering (year, month, quarter)
* No function calls → better performance
* Consistent reporting

Example:

```sql
dim_date(year, month, month_name, quarter)
```

---

## 1️⃣4️⃣ Slowly Changing Dimensions (SCD)

### Type 1 – Overwrite

* No history
* Example: name correction

### Type 2 – History preserved

* New row per change
* Start date / end date
* Active flag

### Type 3 – Limited history

* Old + new column

📌 **Most used: SCD Type 2**

---

## 1️⃣5️⃣ Handling NULLs & Unknowns

Best practice:

* Use **default dimension rows**
* Example:

  * customer_key = 0 → “Unknown Customer”

👉 Avoid NULL foreign keys in facts

---

## 1️⃣6️⃣ Data Modelling in ETL / ELT

### Typical Flow

```
Source → Raw → Staging → Dimensions → Facts → BI
```

### Order:

1. Load dimensions
2. Generate surrogate keys
3. Load facts using dimension keys

---

## 1️⃣7️⃣ Performance Best Practices

* Use integer surrogate keys
* Partition fact tables by date
* Index foreign keys
* Avoid calculated fields in queries
* Pre-aggregate if needed

---

## 1️⃣8️⃣ Common Interview Questions & Answers

### Q: Why fact table is huge?

> Because it stores transactional data at lowest grain.

### Q: Can fact table join to another fact?

> No. Facts join only to dimensions.

### Q: Can dimensions join to dimensions?

> No. Only via fact tables.

### Q: What happens if grain changes?

> Model must be redesigned.

---

## 1️⃣9️⃣ How YOU should explain in interview (Perfect Answer)

> *“We use dimensional modelling with a star schema.
> Facts store measurable business events like sales, dimensions store descriptive context like customer, product, and date.
> We define grain upfront, use surrogate keys, handle SCD Type 2 for history, and optimize for analytics and BI reporting.”*

---

## 2️⃣0️⃣ Final Takeaway

If you understand:

* Grain
* Fact vs Dimension
* Star schema
* Surrogate keys
* SCD Type 2

👉 You are **interview-ready for data modelling**

---
