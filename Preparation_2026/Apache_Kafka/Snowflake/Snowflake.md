
H

# 1. What is Snowflake

**Snowflake** is a **cloud-based data warehouse** used to store and analyze large amounts of data for analytics and reporting.

It runs on cloud platforms like:

* Amazon Web Services
* Microsoft Azure
* Google Cloud Platform

### Simple Idea

Snowflake is used by companies to:

* store large datasets
* run SQL queries
* build dashboards
* perform analytics

Think of it like:

```
Very powerful SQL database
built for cloud analytics
```

---

### Key Concept

Snowflake separates:

```
Storage → where data is stored
Compute → machines that process queries
```

This allows  **independent scaling** .

Example:

```
Storage can grow to petabytes
Compute can scale when needed
```

---

### Short Interview Answer

> Snowflake is a cloud-native data warehouse used for storing and analyzing large-scale data. It separates compute and storage, enabling scalable and efficient analytics.

---

# 2. Snowflake Architecture

Snowflake architecture has  **three main layers** .

```
Client
   ↓
Cloud Services Layer
   ↓
Compute Layer (Virtual Warehouse)
   ↓
Storage Layer
```

---

# 1️⃣ Storage Layer

This layer stores all the data.

Snowflake stores data in  **compressed columnar format** .

Data is stored in cloud storage services such as:

* AWS S3
* Azure Blob
* Google Cloud Storage

Snowflake automatically:

* compresses data
* encrypts data
* divides data into micro-partitions

---

# 2️⃣ Compute Layer (Virtual Warehouse)

This layer  **executes queries and processes data** .

Compute resources are called  **Virtual Warehouses** .

Example sizes:

```
X-Small
Small
Medium
Large
```

Larger warehouses = more CPU and memory.

---

### Example Query Flow

```
User runs SQL query
      ↓
Cloud Services Layer receives query
      ↓
Virtual Warehouse processes query
      ↓
Reads data from storage
      ↓
Returns result
```

---

# 3️⃣ Cloud Services Layer

This layer manages everything.

It handles:

* authentication
* query optimization
* metadata management
* access control
* transaction management

Think of it as  **the brain of Snowflake** .

---

### Short Interview Answer

> Snowflake architecture consists of three layers: the Storage Layer where data is stored, the Compute Layer using virtual warehouses to execute queries, and the Cloud Services Layer which manages query optimization, security, and metadata.

---

# 3. Snowflake Key Features

Snowflake provides several important features.

---

# 1️⃣ Separation of Compute and Storage

Compute and storage scale independently.

Benefits:

```
Better performance
Cost efficiency
Multiple workloads can run simultaneously
```

Example:

```
Analytics team running queries
ETL pipelines running simultaneously
```

---

# 2️⃣ Automatic Scaling

Snowflake can automatically increase compute resources when workload increases.

Example:

```
More users running queries
→ Snowflake adds more compute clusters
```

---

# 3️⃣ Time Travel

Allows users to access  **previous versions of data** .

Example:

```sql
UNDROP TABLE orders;
```

You can restore deleted tables.

Retention period:

```
Standard edition → 1 day
Enterprise edition → up to 90 days
```

---

# 4️⃣ Secure Data Sharing

Snowflake allows sharing data between accounts  **without copying data** .

Example:

```
Company A shares data with Company B
without exporting files
```

---

### Short Interview Answer

> Key Snowflake features include separation of compute and storage, automatic scaling, Time Travel for recovering historical data, and secure data sharing between accounts.

---

# 4. Zero Copy Cloning

## Definition

Zero Copy Cloning allows you to  **create an instant copy of a table, schema, or database without copying the actual data** .

---

## How It Works

Snowflake creates  **metadata pointers to the same storage** .

Example:

```
Original Table
      ↓
Clone Table
```

Both point to the same data.

No physical copy is created.

---

## What Happens When Data Changes

Snowflake uses  **Copy-on-Write** .

Meaning:

```
If data changes
→ new micro-partitions created
→ clone and original diverge
```

---

## Example

```sql
CREATE TABLE orders_clone
CLONE orders;
```

This creates an instant copy.

---

## Use Cases

Zero Copy Cloning is used for:

```
Testing
Development
Backup
Experimentation
```

Example:

```
Production DB
     ↓
Clone for testing
```

---

## Short Interview Answer

> Zero Copy Cloning allows Snowflake to create instant copies of tables or databases without duplicating the underlying data. It works by creating metadata pointers to the same storage and uses copy-on-write when data changes.

---

# 5. Snowflake Tables

Snowflake supports  **three types of tables** .

---

# 1️⃣ Permanent Tables

Default table type.

Features:

```
Supports Time Travel
Supports Fail-safe recovery
Used for production data
```

Example:

```sql
CREATE TABLE customers (
 id INT,
 name STRING
);
```

---

# 2️⃣ Temporary Tables

Temporary tables exist only  **during the current session** .

When session ends → table is automatically deleted.

Features:

```
Visible only to that session
Used for intermediate calculations
```

Example:

```sql
CREATE TEMP TABLE temp_sales;
```

---

# 3️⃣ Transient Tables

Transient tables are similar to permanent tables but  **do not support Fail-safe** .

Benefits:

```
Lower storage cost
Used for staging data
```

Example:

```sql
CREATE TRANSIENT TABLE stage_orders;
```

---

# Table Comparison

| Table Type | Time Travel | Fail-safe | Use Case           |
| ---------- | ----------- | --------- | ------------------ |
| Permanent  | Yes         | Yes       | Production data    |
| Temporary  | Limited     | No        | Session processing |
| Transient  | Yes         | No        | Staging data       |

---

# Short Interview Answer

> Snowflake supports three types of tables: Permanent tables for long-term data storage, Temporary tables which exist only during a session, and Transient tables used for staging data without fail-safe recovery.

---

If you want, I can also give you **one final Snowflake “1-page interview cheat sheet”** that summarizes **all Snowflake concepts in this chat** so you can revise everything in  **10 minutes before the interview** .



---

# 1. Micro-Partitions (Very Important)

## Definition

In Snowflake, data is automatically divided into  **small storage units called micro-partitions** .

Size of each partition:

```
50 MB – 500 MB (compressed)
```

Users **do not manage partitions manually** — Snowflake does it automatically.

---

## How It Works

When data is loaded into Snowflake:

```
Load Data
   ↓
Snowflake converts it to column format
   ↓
Data split into micro-partitions
   ↓
Metadata stored for each partition
```

Each micro-partition stores metadata such as:

```
Minimum value
Maximum value
Distinct count
Null count
```

---

## Example

Suppose a table:

```
orders
```

Snowflake stores it like:

```
Partition 1 → Jan orders
Partition 2 → Feb orders
Partition 3 → Mar orders
```

Query:

```sql
SELECT * FROM orders
WHERE order_date = '2025-01-01';
```

Snowflake reads  **only the relevant partition** .

This is called  **Partition Pruning** .

---

## Important Interview Points

* Created automatically
* Stored in columnar format
* Size 50–500 MB
* Immutable (cannot be modified)
* Improves query performance

---

## Short Interview Answer

> Micro-partitions are Snowflake’s internal storage units that automatically divide table data into small columnar partitions. Each partition stores metadata like min and max values which allows Snowflake to perform partition pruning and improve query performance.

---

# 2. Snowpipe

## Definition

Snowpipe is a feature that  **automatically loads new files from cloud storage into Snowflake tables in near real time** .

---

## How It Works

```
File arrives in cloud storage
      ↓
Event notification triggered
      ↓
Snowpipe activates
      ↓
COPY INTO runs automatically
      ↓
Data loaded into table
```

---

## Example

Create pipe:

```sql
CREATE PIPE sales_pipe AS
COPY INTO sales_table
FROM @sales_stage
FILE_FORMAT = (TYPE = CSV);
```

Whenever new files arrive in stage → Snowpipe loads them automatically.

---

## Key Interview Points

* Continuous data ingestion
* Uses serverless compute
* Triggered by event notifications
* Used for near real-time pipelines

---

## Short Interview Answer

> Snowpipe is Snowflake’s continuous data ingestion service that automatically loads new files from cloud storage into Snowflake tables using event notifications and COPY INTO commands.

---

# 3. Stages (Internal vs External)

## What is a Stage

A **Stage** is a location where data files are stored before loading into Snowflake tables.

Stages are used with:

```
COPY INTO
Snowpipe
```

---

# Internal Stage

Files are stored  **inside Snowflake storage** .

Example:

```sql
CREATE STAGE my_stage;
```

Files uploaded using:

```
PUT command
```

Flow:

```
Local file
   ↓
Internal Stage
   ↓
Snowflake table
```

---

# External Stage

Files stored outside Snowflake in cloud storage like:

* Amazon Web Services S3
* Microsoft Azure Blob Storage
* Google Cloud Platform Cloud Storage

Example:

```sql
CREATE STAGE sales_stage
URL='s3://sales-data/'
STORAGE_INTEGRATION = s3_int;
```

---

## Difference

| Feature          | Internal Stage    | External Stage    |
| ---------------- | ----------------- | ----------------- |
| Storage location | Snowflake         | Cloud storage     |
| File upload      | PUT command       | Already in bucket |
| Cost             | Snowflake storage | Cloud storage     |

---

## Short Interview Answer

> A stage in Snowflake is a temporary storage location used for loading files into tables. Internal stages store files inside Snowflake, while external stages reference files stored in cloud storage like S3.

---

# 4. Storage Integration

## Definition

Storage Integration is a  **secure connection between Snowflake and cloud storage** .

It allows Snowflake to access S3 without storing AWS keys.

---

## How It Works

```
Snowflake
   ↓
Storage Integration
   ↓
IAM Role
   ↓
S3 Bucket
```

Snowflake assumes the IAM role to read files.

---

## Example

```sql
CREATE STORAGE INTEGRATION s3_int
TYPE = EXTERNAL_STAGE
STORAGE_PROVIDER = S3
ENABLED = TRUE
STORAGE_ALLOWED_LOCATIONS = ('s3://sales-data/');
```

Then create stage:

```sql
CREATE STAGE sales_stage
URL='s3://sales-data/'
STORAGE_INTEGRATION=s3_int;
```

---

## Key Interview Points

* Uses IAM roles
* No AWS keys stored
* Secure access to S3
* Used for external stages

---

## Short Interview Answer

> Storage integration is a Snowflake object that securely connects Snowflake to cloud storage using IAM roles instead of access keys.

---

# 5. Streams and Tasks

## Streams

### Definition

A **Stream** tracks changes in a table.

It captures:

```
INSERT
UPDATE
DELETE
```

This is used for  **Change Data Capture (CDC)** .

---

### Example

```sql
CREATE STREAM orders_stream
ON TABLE orders;
```

Now stream shows  **only changed rows** .

---

# Tasks

### Definition

Tasks are used to  **schedule SQL queries automatically** .

Example:

```sql
CREATE TASK process_orders
SCHEDULE = '5 MINUTE'
AS
INSERT INTO final_orders
SELECT * FROM orders_stream;
```

---

## Typical Pipeline

```
Source Table
     ↓
Stream tracks changes
     ↓
Task runs periodically
     ↓
Loads data into target table
```

---

## Key Interview Points

* Stream = change tracking
* Task = scheduled job
* Used for incremental pipelines

---

## Short Interview Answer

> Streams capture data changes in tables while Tasks schedule SQL queries. Together they enable incremental data pipelines in Snowflake.

---

# 6. Snowflake Caching

Snowflake uses **three types of caching** to improve query performance.

---

# 1️⃣ Result Cache

If the same query runs again, Snowflake returns the  **cached result** .

Example:

```
SELECT COUNT(*) FROM orders;
```

If run again → Snowflake returns cached result.

---

# 2️⃣ Metadata Cache

Snowflake uses **micro-partition metadata** to skip unnecessary data scans.

This is also called  **partition pruning** .

---

# 3️⃣ Warehouse Cache

Virtual warehouse keeps  **recently accessed data in local SSD** .

Next query reads data faster.

---

## Cache Summary

| Cache Type      | Purpose                             |
| --------------- | ----------------------------------- |
| Result Cache    | reuse previous query result         |
| Metadata Cache  | skip unnecessary partitions         |
| Warehouse Cache | faster access to recently used data |

---

## Short Interview Answer

> Snowflake uses three types of caching: Result Cache to reuse query results, Metadata Cache to skip scanning irrelevant micro-partitions, and Warehouse Cache to store frequently accessed data in compute nodes.

---

# Quick Revision Summary

Important Snowflake concepts:

```
Micro-partitions → internal storage units
Snowpipe → continuous data ingestion
Stages → file storage before loading
Storage Integration → secure S3 access
Streams → track table changes
Tasks → schedule SQL jobs
Caching → improves query performance
```

---


# 1. Information Schema

## Definition

**Information Schema is a set of system views in Snowflake that store metadata about database objects.**

Metadata means  **data about data** .

In Snowflake, it stores information about:

```
Tables
Columns
Views
Stages
Pipes
Tasks
Privileges
Query history
```

---

## Example

You can check tables in a schema:

```sql
SELECT *
FROM INFORMATION_SCHEMA.TABLES;
```

Check columns in a table:

```sql
SELECT *
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'ORDERS';
```

---

## Common Information Schema Views

| View         | Purpose           |
| ------------ | ----------------- |
| TABLES       | list tables       |
| COLUMNS      | list columns      |
| SCHEMATA     | list schemas      |
| STAGES       | stage metadata    |
| PIPES        | snowpipe metadata |
| LOAD_HISTORY | file load history |

---

## Example (Snowpipe file tracking)

```sql
SELECT *
FROM INFORMATION_SCHEMA.LOAD_HISTORY;
```

Shows which files Snowpipe loaded.

---

## Short Interview Answer

> Information Schema in Snowflake is a set of system views that store metadata about database objects such as tables, columns, stages, and pipes.

---

# 2. Snowflake Data Sharing

## Definition

Snowflake allows  **secure data sharing between Snowflake accounts without copying data** .

This is called  **Secure Data Sharing** .

---

## How It Works

```
Provider Account
        ↓
Share Object
        ↓
Consumer Account
```

The consumer can  **query the data directly** .

No ETL needed.

---

## Example

Create share:

```sql
CREATE SHARE sales_share;
```

Grant access:

```sql
GRANT SELECT ON TABLE sales TO SHARE sales_share;
```

---

## Advantages

```
No data duplication
Real-time data access
Very fast sharing
```

---

## Short Interview Answer

> Snowflake Secure Data Sharing allows data to be shared across Snowflake accounts without copying the data, using shared metadata access.

---

# 3. Snowflake Query History

Snowflake keeps  **history of executed queries** .

You can check using:

```sql
SELECT *
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY());
```

This shows:

```
Query text
Execution time
User
Warehouse used
Status
```

Useful for:

```
Performance tuning
Monitoring
Debugging
```

---

# 4. Snowflake Warehouses

## Definition

A **Virtual Warehouse** is the compute resource used to run queries.

---

## Warehouse Sizes

```
X-Small
Small
Medium
Large
X-Large
```

Larger warehouses → more CPU and memory.

---

## Important Properties

### Auto Suspend

Stops warehouse when idle.

Example:

```sql
AUTO_SUSPEND = 60
```

Warehouse stops after  **60 seconds idle** .

---

### Auto Resume

Warehouse automatically starts when a query arrives.

---

## Short Interview Answer

> A Virtual Warehouse in Snowflake is a compute cluster used to execute SQL queries and perform data processing.

---

# 5. Snowflake Roles (RBAC)

Snowflake uses  **Role-Based Access Control (RBAC)** .

Structure:

```
User
   ↓
Role
   ↓
Privileges
   ↓
Objects
```

Example:

```sql
GRANT SELECT ON TABLE orders TO ROLE analyst;
```

---

## Key Roles

Common roles:

```
ACCOUNTADMIN
SYSADMIN
SECURITYADMIN
PUBLIC
```

---

## Short Interview Answer

> Snowflake uses role-based access control where privileges are assigned to roles and roles are assigned to users.

---

# 6. Snowflake File Formats

Snowflake supports different file formats when loading data.

Example:

```
CSV
JSON
PARQUET
AVRO
ORC
```

Example:

```sql
CREATE FILE FORMAT my_csv_format
TYPE = CSV
FIELD_DELIMITER = ',';
```

Used with:

```
COPY INTO
Snowpipe
```

---

# 7. Snowflake Clustering

Clustering improves query performance on  **large tables** .

Example:

```sql
ALTER TABLE orders
CLUSTER BY(order_date);
```

Snowflake organizes micro-partitions based on the column.

---

## When to Use

Clustering is useful when:

```
Very large tables
Frequent filtering on certain columns
```

---

# 8. Snowflake Fail-safe (Quick Revision)

Fail-safe is the  **last recovery mechanism after Time Travel expires** .

Timeline:

```
Data deleted
     ↓
Time Travel
     ↓
Fail-safe (7 days)
     ↓
Permanent deletion
```

Only Snowflake support can restore data during Fail-safe.

---

# Quick Snowflake Revision Summary

Important Snowflake concepts:

```
Snowflake architecture → storage, compute, cloud services
Micro-partitions → internal storage units
Snowpipe → automatic file ingestion
Stages → file storage before loading
Storage integration → secure S3 access
Streams → track table changes
Tasks → schedule SQL jobs
Caching → improve query performance
Information schema → metadata views
Data sharing → share data without copying
Warehouses → compute resources
RBAC → role-based access control
```
