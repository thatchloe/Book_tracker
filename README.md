# Book Tracker fullstack

This project has:

- **Backend**: FastAPI server + SQLite (`backend/`)
- **Frontend**: static HTML/CSS/JS (`frontend/`)

## Prerequisites

- **Python 3.8+**

## Backend (API server)

### 1) Create and activate a virtual environment

From the project root:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2) Installation

## For backend
```bash
pip install -r requirements.txt
```

### 3) Google Books API key

Generate a Book API key in your Google API account, then create a `backend/.env` file anad save your key inside the file:

```bash

GOOGLE_BOOKS_API_KEY=YOUR_KEY_HERE

```

### 4) Run the backend server

Run from inside `backend/`

```bash
cd backend
uvicorn main:app --reload 
```

- Interactive docs: `http://localhost:8000/docs`

### 5) Run frontend server (client)
Go to `frontend/` and run in a new terminal :

```bash
cd frontend
python3 -m http.server 5173
```

Then open:

- `http://localhost:5173`


