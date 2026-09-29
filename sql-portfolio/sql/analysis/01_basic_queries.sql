-- 01_basic_queries.sql
-- Basic SELECT, WHERE, ORDER BY, LIMIT queries


-- 1. View all customers
SELECT *
FROM customers;


-- 2. Select specific columns
SELECT
    customer_id,
    name,
    country
FROM customers;


-- 3. Find customers from the USA
SELECT
    customer_id,
    name,
    country
FROM customers
WHERE country = 'USA';


-- 4. Find orders over $100
SELECT
    order_id,
    customer_id,
    order_date,
    total_amount
FROM orders
WHERE total_amount > 100;


-- 5. Find orders between $100 and $200
SELECT
    order_id,
    customer_id,
    order_date,
    total_amount
FROM orders
WHERE total_amount BETWEEN 100 AND 200;


-- 6. Find orders placed after September 1, 2026
SELECT
    order_id,
    customer_id,
    order_date,
    total_amount
FROM orders
WHERE order_date > '2026-09-01';


-- 7. Sort orders by amount (highest first)
SELECT
    order_id,
    customer_id,
    order_date,
    total_amount
FROM orders
ORDER BY total_amount DESC;


-- 8. Show the three largest orders
SELECT
    order_id,
    customer_id,
    order_date,
    total_amount
FROM orders
ORDER BY total_amount DESC
LIMIT 3;


-- 9. Find customers whose name starts with "A"
SELECT
    customer_id,
    name,
    country
FROM customers
WHERE name LIKE 'A%';


-- 10. Find orders with an amount of $100 or more
SELECT
    order_id,
    customer_id,
    order_date,
    total_amount
FROM orders
WHERE total_amount >= 100
ORDER BY total_amount DESC;

