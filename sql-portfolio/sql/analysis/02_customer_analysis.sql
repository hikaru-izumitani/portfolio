-- 02_customer_analysis.sql
-- Customer-level analysis using JOIN, GROUP BY, and aggregate functions


-- 1. Show each customer with their orders
SELECT
    c.customer_id,
    c.name,
    o.order_id,
    o.order_date,
    o.total_amount
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
ORDER BY c.customer_id, o.order_date;


-- 2. Count the number of orders for each customer
SELECT
    c.customer_id,
    c.name,
    COUNT(o.order_id) AS order_count
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY order_count DESC;


-- 3. Calculate total spending for each customer
SELECT
    c.customer_id,
    c.name,
    SUM(o.total_amount) AS total_spent
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC;


-- 4. Calculate average order value for each customer
SELECT
    c.customer_id,
    c.name,
    AVG(o.total_amount) AS average_order_value
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY average_order_value DESC;


-- 5. Find the largest order for each customer
SELECT
    c.customer_id,
    c.name,
    MAX(o.total_amount) AS largest_order
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY largest_order DESC;


-- 6. Find customers who placed at least two orders
SELECT
    c.customer_id,
    c.name,
    COUNT(o.order_id) AS order_count
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
HAVING COUNT(o.order_id) >= 2
ORDER BY order_count DESC;


-- 7. Find customers who spent more than $200
SELECT
    c.customer_id,
    c.name,
    SUM(o.total_amount) AS total_spent
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
HAVING SUM(o.total_amount) > 200
ORDER BY total_spent DESC;


-- 8. Compare customer spending by country
SELECT
    c.country,
    COUNT(DISTINCT c.customer_id) AS customer_count,
    SUM(o.total_amount) AS total_revenue,
    AVG(o.total_amount) AS average_order_value
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.country
ORDER BY total_revenue DESC;


-- 9. Find each customer's first and most recent order
SELECT
    c.customer_id,
    c.name,
    MIN(o.order_date) AS first_order_date,
    MAX(o.order_date) AS most_recent_order_date
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY most_recent_order_date DESC;


-- 10. Create a simple customer summary
SELECT
    c.customer_id,
    c.name,
    c.country,
    COUNT(o.order_id) AS order_count,
    SUM(o.total_amount) AS total_spent,
    AVG(o.total_amount) AS average_order_value,
    MAX(o.order_date) AS most_recent_order_date
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.name,
    c.country
ORDER BY total_spent DESC;
