# SQL E-commerce Analysis

A small SQLite project demonstrating fundamental and intermediate SQL skills through e-commerce data analysis.

## Tested Environments

The SQL scripts were tested successfully in the following environments:

- macOS 27.0
  - SQLite 3.54.0
- Ubuntu 26.04.1 LTS on AWS EC2
  - SQLite 3.46.1

## Project Structure

```text
sql-ecommerce-analysis/
├── sql/
│   ├── schema.sql
│   ├── seed.sql
│   ├── 01_basic_queries.sql
│   ├── 02_customer_analysis.sql
│   ├── 03_sales_analysis.sql
│   └── 04_window_functions.sql
├── .gitignore
└── README.md
```

## Requirements

- SQLite 3
- Terminal / Command Line

SQLite is included by default on macOS.
On Ubuntu, install it with:
```bash
sudo apt update
sudo apt install sqlite3
```
## Requirements

* SQLite 3
* Terminal / Command Line

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/hikaru-izumitani/portfolio.git
cd portfolio/sql-portfolio
```

### 2. Create the SQLite database

Run the schema file to create the tables:

```bash
sqlite3 ecommerce.db < sql/schema.sql
```

### 3. Insert sample data

Run the seed file:

```bash
sqlite3 ecommerce.db < sql/seed.sql
```

At this point, the database is ready for analysis.

### 4. Run the basic queries

```bash
sqlite3 ecommerce.db < sql/analysis/01_basic_queries.sql
```

### 5. Run customer analysis

```bash
sqlite3 ecommerce.db < sql/analysis/02_customer_analysis.sql
```

### 6. Run sales analysis

```bash
sqlite3 ecommerce.db < sql/analysis/03_sales_analysis.sql
```

### 7. Run window function analysis

```bash
sqlite3 ecommerce.db < sql/analysis/04_window_functions.sql
```

## Interactive Mode

You can also open the database interactively:

```bash
sqlite3 ecommerce.db
```

Then run SQL queries directly:

```sql
SELECT *
FROM customers;
```

To see all tables:

```sql
.tables
```

To exit SQLite:

```text
.quit
```

## SQL Skills Demonstrated

* SELECT and filtering
* ORDER BY and LIMIT
* JOIN
* GROUP BY and HAVING
* Aggregate functions
* CASE expressions
* Common Table Expressions (CTEs)
* Window functions
* ROW_NUMBER()
* RANK()
* DENSE_RANK()
* LAG() and LEAD()
* Date functions
* Customer and sales analysis

## Reproducibility

The SQLite database file is generated locally from `schema.sql` and `seed.sql`.

This allows the project to be reproduced from scratch without storing the generated database file in the repository.
