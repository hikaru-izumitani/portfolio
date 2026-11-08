# User REST API

A small Flask API for creating, reading, updating, and deleting users in SQLite.

## Tested Environments

- macOS 27.2
  - Python 3.14

## Project Structure

```text
rest-api/
├── requirements.txt
├── rest_api/
│   ├── app.py
│   ├── config.py
│   ├── controllers/
│   ├── models/
│   ├── routes/
│   └── services/database/
└── tests/
```

## Requirements

- Python 3.11 or newer
- The packages in `requirements.txt`

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/hikaru-izumitani/portfolio.git
cd portfolio/rest-api
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Start the API

```bash
python -m rest_api.app
```

The API listens on `http://127.0.0.1:5000`. Users are stored in `instance/users.db`.

### 4. Create a user

```bash
curl -s -X POST http://127.0.0.1:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Ada", "email": "ada@example.com"}'
```

The response includes `id`, `name`, `email`, `created`, `updated`, and `message`.

### 5. Read users

List every user:

```bash
curl -s http://127.0.0.1:5000/users
```

Read one user:

```bash
curl -s http://127.0.0.1:5000/users/<id>
```

An unknown id returns 404. An empty collection also returns 404 with `User not found`.

### 6. Update a user

`PATCH` changes the fields you send. `name` or `email` is enough.

```bash
curl -s -X PATCH http://127.0.0.1:5000/users/<id> \
  -H "Content-Type: application/json" \
  -d '{"name": "Ada Lovelace"}'
```

`PUT` replaces the user and requires both `name` and `email`.

```bash
curl -s -X PUT http://127.0.0.1:5000/users/<id> \
  -H "Content-Type: application/json" \
  -d '{"name": "Grace", "email": "grace@example.com"}'
```

A duplicate email returns 400 with `the email is already in use`. An email without `@` returns 400 with `Invalid email format`.

### 7. Delete a user

```bash
curl -s -X DELETE http://127.0.0.1:5000/users/<id>
```

### 8. Run the tests

```bash
pytest
```

## What this demonstrates

- A Flask REST API for one resource
- `POST`, `GET`, `PATCH`, `PUT`, and `DELETE`
- SQLite persistence through Flask-SQLAlchemy
- Email format checks and a unique email constraint
- 400 for invalid input and 404 for a missing user
- pytest coverage of each route

## Reproducibility

`instance/users.db` is created locally and is not stored in the repository. The tests use a temporary database, so they do not depend on that file.
