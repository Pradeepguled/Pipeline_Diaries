# Databricks Overview & Architecture

## What is Databricks?

Databricks is a platform used to **store, process, transform, and analyze large amounts of data**.

It provides everything in one place:

* Data storage
* Data processing
* SQL queries
* Data pipelines
* Scheduling
* Monitoring

Think of Databricks as a **complete workplace for data engineers**.

---

## Why Do We Need Databricks?

Imagine a company receives millions of records every day:

* Customer data
* Transactions
* Orders
* Logs

Processing such huge data on a normal machine is difficult.

Databricks helps:

* Process large volumes of data quickly
* Handle distributed computing automatically
* Build reliable data pipelines
* Work with teams efficiently

---

## Databricks Architecture (Simple View)

```text
Source Systems
(CSV, JSON, APIs, Database)
            |
            v
      Databricks
            |
    +----------------+
    |   Notebooks    |
    |   SQL Queries  |
    |   Workflows    |
    +----------------+
            |
            v
      Apache Spark
   (Processing Engine)
            |
            v
      Delta Lake
     (Data Storage)
            |
            v
      Reports / BI
```

---

## Main Components of Databricks Architecture

### 1. Workspace

The workspace is where users work.

It contains:

* Notebooks
* Dashboards
* Jobs
* Folders
* Repos

Think of it as your **office desk** inside Databricks.

---

### 2. Notebook

A notebook is where we write:

* Python
* SQL
* Scala
* R

Used to:

* Read data
* Transform data
* Create tables
* Run analysis

Think of it as your **coding notebook**.

---

### 3. Cluster

A cluster provides computing power.

Without a cluster:

* Code cannot run

A cluster consists of multiple machines working together.

Think of it as the **engine of Databricks**.

---

### 4. Apache Spark

Spark is the actual processing engine.

It performs:

* Filtering
* Joins
* Aggregations
* Transformations

Databricks is built on top of Spark.

**Spark does the work. Databricks makes it easy to use.**

---

### 5. Delta Lake

Delta Lake is the storage layer used by Databricks.

It stores data in a reliable format and provides:

* ACID transactions
* Time travel
* Schema enforcement
* Faster queries

Think of Delta Lake as a **smart storage system**.

---

### 6. Workflows / Jobs

Used to automate tasks.

Example:

* Run notebook every day at 6 AM
* Load daily customer data

No manual execution needed.

---

### 7. Unity Catalog

Used for:

* Security
* Governance
* Access control

It controls:

* Who can see data
* Who can modify data
* Who can run jobs

Think of it as the **security guard of Databricks**.

---

## High-Level Data Flow

```text
Source Data
(Database, API, Files)
          |
          v
     Databricks
          |
      Notebook
          |
      Spark Engine
          |
     Delta Tables
          |
      SQL Queries
          |
      Dashboard
```

---

## Simple Real-Life Example

A bank receives credit card transactions daily.

### Step 1

Read transaction files from source.

### Step 2

Spark cleans and transforms data.

### Step 3

Store cleaned data in Delta tables.

### Step 4

Create reports using SQL.

### Step 5

Schedule the entire process using Workflows.

---

## Important Points

* Databricks is built on Apache Spark.
* Clusters provide compute power.
* Notebooks contain code.
* Delta Lake stores data.
* Workflows automate execution.
* Unity Catalog manages security and governance.

---

## Interview One-Liner

**Databricks is a cloud-based data platform built on Apache Spark that provides integrated tools for data engineering, analytics, machine learning, and data governance.**

---

## My Quick Notes

* Databricks = Complete platform for data processing.
* Spark = Processing engine.
* Cluster = Compute power.
* Notebook = Place to write code.
* Delta Lake = Storage layer.
* Workflows = Automation.
* Unity Catalog = Security & governance.
