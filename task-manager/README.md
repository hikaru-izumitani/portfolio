# Task Manager

A small full-stack task app. The Expo web app has a task list and a summary page. Adding a task sends it to a Django REST API, which stores it in SQLite. Both pages read the same Redux store.

## Tested Environments

- macOS 27
  - Python 3.14
  - Node.js with Expo SDK 58

## Project Structure

```text
task-manager/
├── requirements.txt
├── backend/
│   ├── manage.py
│   ├── customers/
│   └── myproject/
└── frontend/
    ├── app/
    ├── components/
    ├── store/
    └── package.json
```

## Requirements

- Python 3.12 or newer
- Node.js 20 or newer
- The packages in `requirements.txt`

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/hikaru-izumitani/portfolio.git
cd portfolio/task-manager
```

### 2. Create a virtual environment and start the API

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd backend
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000
```

The task endpoint is `http://127.0.0.1:8000/api/tasks/`.

Create a task:

```bash
curl -s -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk", "completed": false}'
```

List tasks:

```bash
curl -s http://127.0.0.1:8000/api/tasks/
```

### 3. Start the app

In a second terminal:

```bash
cd portfolio/task-manager/frontend
npm install
npx expo start
```

Press `w` to open the app at `http://localhost:8081`.

Type a title and press Add Task. The new task appears in the list. Open Summary to see the total, completed, and remaining counts. Completed and deleted tasks change in the app only. The API stores the title and the completed flag sent when the task is created.

## What this demonstrates

- An Expo Router app with two screens
- A Redux store shared by both screens
- `GET` and `POST` through Redux thunks
- A Django REST Framework list-and-create endpoint
- SQLite persistence for tasks
- A web UI that updates from the stored tasks

## Reproducibility

`backend/db.sqlite3` and `frontend/node_modules/` are created locally and are not stored in the repository. Run `migrate` before starting the API.
