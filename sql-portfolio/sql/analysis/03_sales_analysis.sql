-- 03_sales_analysis.sql
-- Sales analysis using aggregation, CASE, CTEs, and window functions


-- 1. Calculate total revenue
SELECT
    SUM(total_amount) AS total_revenue
FROM orders;


-- 2. Calculate the number of orders
SELECT
    COUNT(*) AS total_orders
FROM orders;


-- 3. Calculate average order value
SELECT
    AVG(total_amount) AS average_order_value
FROM orders;


-- 4. Calculate total revenue by date
SELECT
    order_date,
    SUM(total_amount) AS daily_revenue
FROM orders
GROUP BY order_date
ORDER BY order_date;


-- 5. Calculate monthly revenue
SELECT
    strftime('%Y-%m', order_date) AS month,
    SUM(total_amount) AS monthly_revenue
FROM orders
GROUP BY month
ORDER BY month;


-- 6. Find the highest-revenue day
SELECT
    order_date,
    SUM(total_amount) AS daily_revenue
FROM orders
GROUP BY order_date
ORDER BY daily_revenue DESC
LIMIT 1;


-- 7. Rank individual orders by amount
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


-- 8. Classify orders by size
SELECT
    order_id,
    customer_id,
    total_amount,
    CASE
        WHEN total_amount >= 200 THEN 'Large'
        WHEN total_amount >= 100 THEN 'Medium'
        ELSE 'Small'
    END AS order_category
FROM orders
ORDER BY total_amount DESC;


-- 9. Count orders by size category
WITH classified_orders AS (
    SELECT
        order_id,
        total_amount,
        CASE
            WHEN total_amount >= 200 THEN 'Large'
            WHEN total_amount >= 100 THEN 'Medium'
            ELSE 'Small'
        END AS order_category
    FROM orders
)
SELECT
    order_category,
    COUNT(*) AS order_count,
    SUM(total_amount) AS total_revenue
FROM classified_orders
GROUP BY order_category
ORDER BY total_revenue DESC;


-- 10. Calculate cumulative revenue over time
WITH daily_sales AS (
    SELECT
        order_date,
        SUM(total_amount) AS daily_revenue
    FROM orders
    GROUP BY order_date
)
SELECT
    order_date,
    daily_revenue,
    SUM(daily_revenue) OVER (
        ORDER BY order_date
    ) AS cumulative_revenue
FROM daily_sales
ORDER BY order_date;


-- 11. Compare each order with the average order value
SELECT
    order_id,
    customer_id,
    total_amount,
    AVG(total_amount) OVER () AS overall_average,
    total_amount - AVG(total_amount) OVER () AS difference_from_average
FROM orders
ORDER BY total_amount DESC;


-- 12. Calculate revenue by country
SELECT
    c.country,
    COUNT(o.order_id) AS order_count,
    SUM(o.total_amount) AS total_revenue,
    AVG(o.total_amount) AS average_order_value
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.country
ORDER BY total_revenue DESC;


-- 13. Calculate each country's percentage of total revenue
WITH country_sales AS (
    SELECT
        c.country,
        SUM(o.total_amount) AS revenue
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY c.country
)
SELECT
    country,
    revenue,
    ROUND(
        revenue * 100.0 /
        SUM(revenue) OVER (),
        2
    ) AS revenue_percentage
FROM country_sales
ORDER BY revenue DESC;
