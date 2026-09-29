-- schema.sql
-- Database schema for the SQL E-commerce Analysis project


-- Remove existing tables so the database can be rebuilt from scratch
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;


-- Customers table
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    country TEXT NOT NULL
);


-- Orders table
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    total_amount REAL NOT NULL,

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);
