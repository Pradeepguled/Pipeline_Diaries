Here are **50 SQL interview questions rewritten for the dimensional (star) model** we created:

Tables to use:

* **Facts:** `fact_sales`, `fact_sales_item`
* **Dims:** `dim_date`, `dim_customer`, `dim_product`, `dim_employee`, `dim_department`

---

## 1) SELECT & FILTERING (1–10)

1. Fetch all rows from `fact_sales`.
2. Fetch `order_id`, `status`, `total_amount` from `fact_sales`.
3. Fetch all delivered orders (`status = 'DELIVERED'`).
4. Fetch all orders placed in March 2024 (use `dim_date`).
5. Fetch all customers from `dim_customer` whose name starts with `A`.
6. Fetch all products from `dim_product` in category `Electronics`.
7. Fetch all employees from `dim_employee` with salary > 80,000.
8. Fetch employees hired in the year 2023.
9. Fetch top 5 highest value orders (by `total_amount`).
10. Fetch all cancelled orders in Feb 2024.

---

## 2) AGGREGATIONS & GROUP BY (11–20)

11. Count total number of orders.
12. Count total number of customers who have placed at least one order.
13. Find total revenue (sum of `total_amount`) overall.
14. Find total revenue per customer.
15. Find total revenue per city (customer city).
16. Find total revenue per month (use `dim_date`).
17. Find number of orders per month.
18. Find average order value (AOV) per customer.
19. Find customers who spent more than 1 lakh total.
20. Find top 3 cities by total revenue.

---

## 3) JOINS (21–30)

21. Show `order_id`, `full_date`, `customer_name`, `status`, `total_amount` (join `fact_sales` with `dim_date` and `dim_customer`).
22. Show all customers and their total spend (include customers with no orders).
23. Find customers who never placed any order (dim to fact anti-join).
24. Show order line items with customer name and product name (join `fact_sales_item` with dims).
25. Show total quantity sold per product name.
26. Show total revenue per product category.
27. Show employees with department name (employee dim + department dim).
28. Show departments with no employees.
29. Show employees who are not assigned to any department.
30. Show employees and their manager names (self join on `dim_employee` using `manager_emp_id` ↔ `emp_id`).

---

## 4) SUBQUERIES (31–38)

31. Find orders whose `total_amount` is greater than the overall average order value.
32. Find customers whose spend is greater than the overall average customer spend.
33. Find products that were never sold.
34. Find customers who placed at least one order (use `EXISTS`).
35. Find customers who never placed any order (use `NOT EXISTS`).
36. Find the customer who has the highest total spend.
37. Find the month with the highest total revenue.
38. Find employees earning more than their department average salary.

---

## 5) WINDOW FUNCTIONS (39–45)

39. Rank customers by total spend (highest to lowest).
40. Show top 3 customers by spend within each city.
41. Rank orders by amount per month.
42. Show running total of revenue by date.
43. For each customer, show previous order amount (LAG) ordered by date.
44. Find day-over-day revenue difference using LAG on daily revenue.
45. For each product, rank months by revenue (best month = rank 1).

---

## 6) CTE (46–50)

46. Using CTE, compute monthly revenue and then return only months where revenue > 50,000.
47. Using CTE, find top 3 products by revenue.
48. Using CTE, find customers who spent more than city average spend.
49. Using CTE + window function, return the highest order per customer.
50. Using recursive CTE, build employee → manager hierarchy (org chart) from `dim_employee`.

---

