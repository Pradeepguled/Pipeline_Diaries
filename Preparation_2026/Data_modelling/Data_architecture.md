
Below is a **clean star schema** for your same use-cases (customers, orders, products, employees/departments), with:

✅ Dimensions (descriptive tables)
✅ Facts (transaction / measures tables)
✅ Supports **all your earlier questions** (joins, aggregations, windows, CTEs)

---

## 1) Star Schema Tables (CREATE TABLE)

### Dim: Date

```sql
CREATE TABLE dim_date (
  date_key      INT PRIMARY KEY,          -- yyyymmdd like 20240105
  full_date     DATE NOT NULL,
  year          INT NOT NULL,
  month         INT NOT NULL,
  month_name    VARCHAR(15) NOT NULL,
  quarter       INT NOT NULL,
  day_of_month  INT NOT NULL,
  day_name      VARCHAR(15) NOT NULL
);
```

### Dim: Customer

```sql
CREATE TABLE dim_customer (
  customer_key   INT PRIMARY KEY,
  customer_id    INT NOT NULL UNIQUE,     -- business id
  customer_name  VARCHAR(120) NOT NULL,
  city           VARCHAR(80),
  signup_date    DATE
);
```

### Dim: Product

```sql
CREATE TABLE dim_product (
  product_key    INT PRIMARY KEY,
  product_id     INT NOT NULL UNIQUE,     -- business id
  product_name   VARCHAR(150) NOT NULL,
  category       VARCHAR(80),
  list_price     NUMERIC(12,2) NOT NULL
);
```

### Dim: Department

```sql
CREATE TABLE dim_department (
  dept_key    INT PRIMARY KEY,
  dept_id     INT NOT NULL UNIQUE,        -- business id
  dept_name   VARCHAR(100) NOT NULL
);
```

### Dim: Employee (includes manager as a dimensional attribute)

```sql
CREATE TABLE dim_employee (
  employee_key   INT PRIMARY KEY,
  emp_id         INT NOT NULL UNIQUE,     -- business id
  emp_name       VARCHAR(100) NOT NULL,
  dept_key       INT NULL,
  manager_emp_id INT NULL,                -- manager business id (self reference)
  hire_date      DATE NOT NULL,
  current_salary NUMERIC(12,2) NOT NULL,

  CONSTRAINT fk_emp_dept_dim
    FOREIGN KEY (dept_key) REFERENCES dim_department(dept_key)
);
```

---

## 2) Fact Tables

### Fact: Sales (order-level fact)

```sql
CREATE TABLE fact_sales (
  sales_key     INT PRIMARY KEY,
  order_id      INT NOT NULL UNIQUE,      -- degenerate dimension (order id)
  date_key      INT NOT NULL,
  customer_key  INT NOT NULL,
  status        VARCHAR(30) NOT NULL,
  total_amount  NUMERIC(12,2) NOT NULL,

  CONSTRAINT fk_sales_date     FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
  CONSTRAINT fk_sales_customer FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key)
);
```

### Fact: Sales Line Items (order-product grain)

```sql
CREATE TABLE fact_sales_item (
  sales_item_key INT PRIMARY KEY,
  order_id       INT NOT NULL,            -- joins to fact_sales.order_id (degenerate)
  date_key       INT NOT NULL,
  customer_key   INT NOT NULL,
  product_key    INT NOT NULL,
  qty            INT NOT NULL,
  unit_price     NUMERIC(12,2) NOT NULL,
  line_amount    NUMERIC(12,2) NOT NULL,

  CONSTRAINT fk_item_date     FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
  CONSTRAINT fk_item_customer FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
  CONSTRAINT fk_item_product  FOREIGN KEY (product_key) REFERENCES dim_product(product_key)
);
```

---

## 3) Sample Data (INSERTS) — small but enough for interviews

### dim_department

```sql
INSERT INTO dim_department (dept_key, dept_id, dept_name) VALUES
(1, 10, 'Data'),
(2, 20, 'Engineering'),
(3, 30, 'HR'),
(4, 40, 'Finance'),
(5, 50, 'Marketing');
```

### dim_employee

```sql
INSERT INTO dim_employee (employee_key, emp_id, emp_name, dept_key, manager_emp_id, hire_date, current_salary) VALUES
(1,  1, 'Amit',   2, NULL, '2020-01-10', 120000),
(2,  2, 'Ravi',   2, 1,    '2021-03-15',  90000),
(3,  3, 'Neha',   2, 1,    '2022-07-20',  90000),
(4,  4, 'Priya',  1, NULL, '2019-11-05', 110000),
(5,  5, 'Kiran',  1, 4,    '2023-01-12',  70000),
(6,  6, 'Sneha',  1, 4,    '2024-02-10',  60000),
(7,  7, 'Rahul',  3, NULL, '2022-04-01',  50000),
(8,  8, 'Anita',  3, 7,    '2023-06-18',  45000),
(9,  9, 'Vikram', NULL, NULL,'2021-09-09', 80000),
(10,10, 'Suresh', 4, NULL, '2020-12-25',  95000);
```

### dim_customer

```sql
INSERT INTO dim_customer (customer_key, customer_id, customer_name, city, signup_date) VALUES
(1, 101, 'Pradeep', 'Bangalore', '2022-01-01'),
(2, 102, 'Aakash',  'Mumbai',    '2022-05-12'),
(3, 103, 'Snehal',  'Pune',      '2023-02-20'),
(4, 104, 'Rohit',   'Delhi',     '2023-08-15'),
(5, 105, 'Megha',   'Chennai',   '2024-01-10');
```

### dim_product

```sql
INSERT INTO dim_product (product_key, product_id, product_name, category, list_price) VALUES
(1, 201, 'Laptop',   'Electronics', 70000),
(2, 202, 'Mouse',    'Electronics',   500),
(3, 203, 'Keyboard', 'Electronics',  1500),
(4, 204, 'Chair',    'Furniture',   4000),
(5, 205, 'Desk',     'Furniture',  10000);
```

### dim_date (only dates we need)

```sql
INSERT INTO dim_date (date_key, full_date, year, month, month_name, quarter, day_of_month, day_name) VALUES
(20240105, '2024-01-05', 2024, 1, 'January', 1, 5,  'Friday'),
(20240210, '2024-02-10', 2024, 2, 'February',1, 10, 'Saturday'),
(20240215, '2024-02-15', 2024, 2, 'February',1, 15, 'Thursday'),
(20240301, '2024-03-01', 2024, 3, 'March',   1, 1,  'Friday'),
(20240310, '2024-03-10', 2024, 3, 'March',   1, 10, 'Sunday'),
(20240315, '2024-03-15', 2024, 3, 'March',   1, 15, 'Friday');
```

### fact_sales (order level)

```sql
INSERT INTO fact_sales (sales_key, order_id, date_key, customer_key, status, total_amount) VALUES
(1, 1001, 20240105, 1, 'DELIVERED', 75000),
(2, 1002, 20240210, 1, 'DELIVERED',  1500),
(3, 1003, 20240215, 2, 'CANCELLED',   500),
(4, 1004, 20240301, 3, 'DELIVERED', 14000),
(5, 1005, 20240310, 3, 'DELIVERED',  4000),
(6, 1006, 20240315, 4, 'DELIVERED', 70000);
```

### fact_sales_item (order-product level)

```sql
INSERT INTO fact_sales_item (sales_item_key, order_id, date_key, customer_key, product_key, qty, unit_price, line_amount) VALUES
(1, 1001, 20240105, 1, 1, 1, 70000, 70000),
(2, 1001, 20240105, 1, 2, 1,   500,   500),
(3, 1001, 20240105, 1, 3, 1,  1500,  1500),
(4, 1002, 20240210, 1, 3, 1,  1500,  1500),
(5, 1003, 20240215, 2, 2, 1,   500,   500),
(6, 1004, 20240301, 3, 5, 1, 10000, 10000),
(7, 1004, 20240301, 3, 4, 1,  4000,  4000),
(8, 1005, 20240310, 3, 4, 1,  4000,  4000),
(9, 1006, 20240315, 4, 1, 1, 70000, 70000);
```

---

## 4) How your earlier queries look in star schema (2 examples)

### Customers who spent > 1 lakh

```sql
SELECT c.customer_name, SUM(s.total_amount) AS total_spent
FROM fact_sales s
JOIN dim_customer c ON c.customer_key = s.customer_key
GROUP BY c.customer_name
HAVING SUM(s.total_amount) > 100000;
```

### Orders with product details

```sql
SELECT i.order_id, c.customer_name, p.product_name, i.qty, i.unit_price, i.line_amount
FROM fact_sales_item i
JOIN dim_customer c ON c.customer_key = i.customer_key
JOIN dim_product  p ON p.product_key  = i.product_key;
```

---
