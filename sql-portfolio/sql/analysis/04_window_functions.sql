-- 04_window_functions.sql
-- Window function analysis
-- Demonstrates ROW_NUMBER, RANK, DENSE_RANK,
-- PARTITION BY, LAG, LEAD, and running totals


-- 1. Rank all orders by amount
SELECT
    order_id,
    customer_id,
    order_date,
    total_amount,
    RANK() OVER (
        ORDER BY total_amount DESC
    ) AS order_rank
FROM orders
ORDER BY order_rank;


-- 2. Assign a unique row number to each order
SELECT
    order_id,
    customer_id,
    order_date,
    total_amount,
    ROW_NUMBER() OVER (
        ORDER BY total_amount DESC
    ) AS row_number
FROM orders
ORDER BY row_number;


-- 3. Compare RANK and DENSE_RANK
SELECT
    order_id,
    total_amount,
    RANK() OVER (
        ORDER BY total_amount DESC
    ) AS rank_value,
    DENSE_RANK() OVER (
        ORDER BY total_amount DESC
    ) AS dense_rank_value
FROM orders
ORDER BY total_amount DESC;


-- 4. Rank orders within each customer
SELECT
    order_id,
    customer_id,
    order_date,
    total_amount,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id
        ORDER BY total_amount DESC
    ) AS customer_order_rank
FROM orders
ORDER BY customer_id, customer_order_rank;


-- 5. Find the largest order for each customer
WITH ranked_orders AS (
    SELECT
        order_id,
        customer_id,
        order_date,
        total_amount,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY total_amount DESC
        ) AS row_num
    FROM orders
)
SELECT
    order_id,
    customer_id,
    order_date,
    total_amount
FROM ranked_orders
WHERE row_num = 1
ORDER BY customer_id;


-- 6. Calculate each customer's cumulative spending
SELECT
    customer_id,
    order_date,
    total_amount,
    SUM(total_amount) OVER (
        PARTITION BY customer_id
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_spending
FROM orders
ORDER BY customer_id, order_date;


-- 7. Calculate overall cumulative revenue
SELECT
    order_id,
    order_date,
    total_amount,
    SUM(total_amount) OVER (
        ORDER BY order_date, order_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_revenue
FROM orders
ORDER BY order_date, order_id;


-- 8. Compare each order with the previous order
SELECT
    order_id,
    customer_id,
    order_date,
    total_amount,
    LAG(total_amount) OVER (
        PARTITION BY customer_id
        ORDER BY order_date, order_id
    ) AS previous_order_amount
FROM orders
ORDER BY customer_id, order_date, order_id;


-- 9. Calculate the change from the previous order
SELECT
    order_id,
    customer_id,
    order_date,
    total_amount,
    LAG(total_amount) OVER (
        PARTITION BY customer_id
        ORDER BY order_date, order_id
    ) AS previous_order_amount,
    total_amount
        - LAG(total_amount) OVER (
            PARTITION BY customer_id
            ORDER BY order_date, order_id
        ) AS amount_change
FROM orders
ORDER BY customer_id, order_date, order_id;


-- 10. Look at the next order for each customer
SELECT
    order_id,
    customer_id,
    order_date,
    total_amount,
    LEAD(order_date) OVER (
        PARTITION BY customer_id
        ORDER BY order_date, order_id
    ) AS next_order_date
FROM orders
ORDER BY customer_id, order_date, order_id;


-- 11. Calculate the average order value for each customer
-- while keeping every individual order
SELECT
    order_id,
    customer_id,
    order_date,
    total_amount,
    AVG(total_amount) OVER (
        PARTITION BY customer_id
    ) AS customer_average_order_value
FROM orders
ORDER BY customer_id, order_date;


-- 12. Compare each order with the customer's average
SELECT
    order_id,
    customer_id,
    order_date,
    total_amount,
    AVG(total_amount) OVER (
        PARTITION BY customer_id
    ) AS customer_average,
    total_amount
        - AVG(total_amount) OVER (
            PARTITION BY customer_id
        ) AS difference_from_customer_average
FROM orders
ORDER BY customer_id, order_date;


-- 13. Calculate the percentage of each order
-- relative to the customer's total spending
SELECT
    order_id,
    customer_id,
    order_date,
    total_amount,
    ROUND(
        total_amount * 100.0 /
        SUM(total_amount) OVER (
            PARTITION BY customer_id
        ),
        2
    ) AS percentage_of_customer_spending
FROM orders
ORDER BY customer_id, order_date;


-- 14. Calculate running revenue by customer
SELECT
    c.name,
    o.order_id,
    o.order_date,
    o.total_amount,
    SUM(o.total_amount) OVER (
        PARTITION BY o.customer_id
        ORDER BY o.order_date, o.order_id
    ) AS cumulative_customer_revenue
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
ORDER BY c.customer_id, o.order_date, o.order_id;


-- 15. Identify each customer's first order
WITH ranked_orders AS (
    SELECT
        order_id,
        customer_id,
        order_date,
        total_amount,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY order_date, order_id
        ) AS row_num
    FROM orders
)
SELECT
    order_id,
    customer_id,
    order_date,
    total_amount
FROM ranked_orders
WHERE row_num = 1
ORDER BY customer_id;
