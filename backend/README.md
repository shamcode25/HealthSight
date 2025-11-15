# Healthcare Analytics Dashboard - Backend

FastAPI backend with SQLAlchemy ORM and SQLite database.

## Setup

### Prerequisites

- Python 3.9 or higher
- pip

### Installation

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Server

#### Option 1: Using run.py
```bash
python run.py
```

#### Option 2: Using uvicorn directly
```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Database

- The database file `healthcare.db` will be automatically created in the backend directory on first run
- The database will be automatically seeded with synthetic data if empty
- To reset the database, simply delete `healthcare.db` and restart the server

### API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### API Endpoints

**Standard Endpoints:**
- `GET /health` - Health check
- `GET /overview-metrics` - Get overview dashboard metrics
- `GET /readmissions/list` - Get list of patient episodes (supports `unit` and `risk_level` query params)
- `GET /readmissions/high-risk` - Get high-risk episodes only
- `GET /readmissions/{episode_id}` - Get specific episode details
- `GET /quality/incidents` - Get all safety incidents
- `GET /quality/incidents/summary` - Get safety incidents summary and KPIs
- `GET /data-quality/issues` - Get all data quality issues
- `GET /data-quality/metrics` - Get data quality metrics and KPIs
- `GET /risk-distribution` - Get risk level distribution
- `GET /health-trends` - Get health trends data

**AI Endpoints (require OPENAI_API_KEY):**
- `POST /llm/summary/{episode_id}` - Generate AI summary for episode
- `POST /llm/risk-explanation/{episode_id}` - Generate AI risk explanation
- `POST /llm/recommendations/{episode_id}` - Generate AI recommendations
- `POST /llm/generate-all/{episode_id}` - Generate all AI insights at once

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Required for AI features
OPENAI_API_KEY=your_openai_api_key_here

# Optional overrides
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.3
DATABASE_URL=sqlite:///./healthcare.db
```

**Important:** You must set `OPENAI_API_KEY` to use AI features. Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys).

You can copy `.env.example` to `.env` and fill in your API key:

```bash
cp .env.example .env
# Then edit .env and add your OPENAI_API_KEY
```

### CORS

The API is configured to allow requests from:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (Alternative frontend port)

To add more origins, update `CORS_ORIGINS` in `src/config.py`.
