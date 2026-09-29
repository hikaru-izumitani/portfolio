CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    country TEXT
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,
    total_amount REAL
);