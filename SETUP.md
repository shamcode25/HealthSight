# Setup Guide

This guide will help you set up and run the Healthcare Analytics Dashboard with the FastAPI backend.

## Prerequisites

- **Node.js 18+** installed
- **Python 3.9+** installed
- **npm** (comes with Node.js)
- **pip** (comes with Python)

## Step-by-Step Setup

### 1. Install Frontend Dependencies

From the project root:
```bash
npm install
```

### 2. Set Up Backend

Navigate to the backend directory:
```bash
cd backend
```

Create a virtual environment (recommended):
```bash
# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
venv\Scripts\activate
```

Install Python dependencies:
```bash
pip install -r requirements.txt
```

### 3. Start the Backend Server

From the `backend` directory:
```bash
python run.py
```

Or using uvicorn directly:
```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
- Database tables being created
- Synthetic data being seeded (500 episodes, 200 incidents, 300 quality issues)
- Server running at `http://localhost:8000`

### 4. Start the Frontend

Open a **new terminal** window/tab and from the project root:
```bash
npm run dev
```

The frontend will start at `http://localhost:5173`

### 5. Access the Dashboard

Open your browser and navigate to:
```
http://localhost:5173
```

## Verify Setup

1. **Backend Health Check:**
   - Visit: `http://localhost:8000/health`
   - Should return: `{"status": "healthy", "timestamp": "..."}`

2. **API Documentation:**
   - Visit: `http://localhost:8000/docs`
   - Should show Swagger UI with all endpoints

3. **Frontend:**
   - Should load the dashboard at `http://localhost:5173`
   - All pages should load data from the backend

## Troubleshooting

### Backend Issues

**Database already exists:**
- If you want to reset the database, delete `backend/healthcare.db` and restart the server

**Port 8000 already in use:**
- Change the port in `backend/run.py` or use: `uvicorn src.api.main:app --reload --port 8001`

**Module not found errors:**
- Make sure you're in the `backend` directory when installing
- Ensure virtual environment is activated
- Try: `pip install -r requirements.txt --upgrade`

### Frontend Issues

**Cannot connect to backend:**
- Ensure backend is running on `http://localhost:8000`
- Check browser console for CORS errors
- Verify `src/services/apiClient.ts` has correct baseURL

**Port 5173 already in use:**
- Vite will automatically try the next available port
- Or specify a port: `npm run dev -- --port 5174`

## Production Build

### Backend
```bash
cd backend
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
npm run build
npm run preview
```

## Next Steps

- Review the API endpoints at `http://localhost:8000/docs`
- Explore the dashboard pages
- Customize the theme in `src/theme/theme.ts`
- Add new endpoints in `backend/src/api/main.py`
- Modify database models in `backend/src/models/db_models.py`
