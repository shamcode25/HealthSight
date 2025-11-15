Publish Functionality---- https://filter-quick-81380443.figma.site/

# Healthcare Analytics Dashboard

A comprehensive healthcare analytics dashboard built with React, TypeScript, Vite, Material-UI, and FastAPI backend with SQLite database.

## Features

- 📊 **Overview Dashboard** - Key metrics and health trends visualization
- 🏥 **Quality & Safety** - Track safety incidents and quality metrics
- 🔄 **Readmissions** - Monitor high-risk patient episodes with detailed risk analysis
- ✅ **Data Quality** - Identify and manage data quality issues across units
- 📈 **Interactive Charts** - Visualize healthcare data with Recharts
- 🎨 **Material-UI Design** - Modern, professional interface matching Figma design
- 🗄️ **SQL Database** - Real SQLite database with synthetic healthcare data
- 🔌 **FastAPI Backend** - RESTful API with automatic database seeding
- 🤖 **AI-Powered Insights** - OpenAI + LangChain integration for:
  - AI-generated patient episode summaries
  - Intelligent risk explanations
  - Personalized next-best-action recommendations

## Tech Stack

### Frontend
- **React 18+** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Material-UI (MUI) + Emotion** - Component library and styling
- **React Router** - Client-side routing
- **Recharts** - Data visualization
- **Axios** - HTTP client

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Lightweight database
- **Pydantic** - Data validation
- **Pandas/NumPy** - Data processing
- **OpenAI** - GPT-4o-mini for AI insights
- **LangChain** - Prompt templating and LLM orchestration

## Project Structure

```
HealthSight/
├── frontend (src/)
│   ├── main.tsx                 # Entry point
│   ├── App.tsx                  # Root component
│   ├── router.tsx               # React Router configuration
│   ├── components/              # React components
│   ├── pages/                   # Page components
│   ├── services/
│   │   └── apiClient.ts         # API client (calls backend)
│   └── types/
│       └── index.ts             # TypeScript types
│
└── backend/
    ├── src/
    │   ├── api/
    │   │   └── main.py          # FastAPI application
    │   ├── models/
    │   │   └── db_models.py     # SQLAlchemy models
    │   ├── schemas/
    │   │   └── api_models.py    # Pydantic schemas
    │   ├── etl/
    │   │   ├── synthetic_data.py # Data generation
    │   │   └── load_data.py      # Database seeding
    │   ├── db.py                # Database setup
    │   └── config.py            # Configuration
    ├── requirements.txt         # Python dependencies
    └── run.py                   # Server startup script
```

## Getting Started

### Prerequisites

- **Node.js 18+** and npm
- **Python 3.9+** and pip
- **OpenAI API Key** (required for AI features) - Get one at [OpenAI Platform](https://platform.openai.com/api-keys)

### Quick Start

1. **Clone the repository** (if applicable)

2. **Start the Backend:**
```bash
cd backend
python -m venv venv  # Create virtual environment (optional but recommended)
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up OpenAI API key (required for AI features)
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY=your_key_here

python run.py
```
The backend will start at `http://localhost:8000`

**Note:** AI features require an OpenAI API key. Without it, the app will work but AI generation will fail. You can get an API key from [OpenAI Platform](https://platform.openai.com/api-keys).

3. **Start the Frontend:**
```bash
# In a new terminal, from the project root
npm install
npm run dev
```
The frontend will start at `http://localhost:5173`

4. **Access the Dashboard:**
Open `http://localhost:5173` in your browser

### Database

- The SQLite database (`healthcare.db`) is automatically created on first backend startup
- The database is automatically seeded with 500 patient episodes, 200 safety incidents, and 300 data quality issues
- To reset the database, delete `backend/healthcare.db` and restart the backend server

### API Documentation

Once the backend is running:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Standard Endpoints

- `GET /health` - Health check
- `GET /overview-metrics` - Overview dashboard KPIs
- `GET /readmissions/list` - Patient episodes (supports `unit` and `risk_level` filters)
- `GET /readmissions/{episode_id}` - Specific episode details
- `GET /quality/incidents` - Safety incidents
- `GET /quality/incidents/summary` - Safety KPIs and category distribution
- `GET /data-quality/issues` - Data quality issues
- `GET /data-quality/metrics` - Data quality KPIs and unit breakdown
- `GET /risk-distribution` - Risk level distribution
- `GET /health-trends` - Health trends over time

### AI Endpoints (require OPENAI_API_KEY)

- `POST /llm/summary/{episode_id}` - Generate AI summary for patient episode
- `POST /llm/risk-explanation/{episode_id}` - Generate AI risk explanation
- `POST /llm/recommendations/{episode_id}` - Generate AI recommendations
- `POST /llm/generate-all/{episode_id}` - Generate all AI insights at once (recommended)

## Pages

- **Overview** (`/overview`) - Main dashboard with KPIs and health trends
- **Quality & Safety** (`/quality-safety`) - Safety incidents and quality metrics
- **Readmissions** (`/readmissions`) - High-risk patient episodes with **AI-powered insights**:
  - Click any episode row to generate AI summary, risk explanation, and recommendations
  - AI insights are automatically saved to the database
  - Real-time loading states and error handling
- **Data Quality** (`/data-quality`) - Data quality issues and metrics by unit

## Development

### Frontend Development
```bash
npm run dev        # Start dev server
npm run build      # Build for production
npm run preview    # Preview production build
```

### Backend Development
```bash
cd backend
python run.py      # Start with auto-reload
# Or
uvicorn src.api.main:app --reload
```

### Environment Variables

**Backend** (`backend/.env`):
```env
# Required for AI features
OPENAI_API_KEY=your_openai_api_key_here

# Optional AI configuration
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.3

# Database (optional override)
DATABASE_URL=sqlite:///./healthcare.db
```

See the [AI Features](#ai-features) section below for more details on AI configuration.

## AI Features

The dashboard includes AI-powered insights using OpenAI's GPT-4o-mini model:

### How It Works

1. **User Interaction**: Click on any patient episode in the Readmissions page
2. **AI Generation**: The system automatically generates:
   - **Patient Summary**: Concise clinical summary of the episode
   - **Risk Explanation**: Evidence-based explanation of readmission risk factors
   - **Recommendations**: Actionable next steps to reduce readmission risk
3. **Storage**: All AI-generated content is saved to the SQLite database
4. **Caching**: Previously generated insights are retrieved from the database

### AI Configuration

Edit `backend/.env` to customize AI settings:

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini          # Default model
OPENAI_TEMPERATURE=0.3             # Lower = more deterministic (0.0-2.0)
```

### AI Modules

- `backend/src/llm/summary.py` - Generates patient episode summaries
- `backend/src/llm/risk_explanation.py` - Explains readmission risks
- `backend/src/llm/recommendations.py` - Provides next-best-action recommendations
- `backend/src/llm/llm_utils.py` - OpenAI/LangChain utilities

### Troubleshooting AI

- **"OpenAI API key not set"**: Ensure `OPENAI_API_KEY` is set in `backend/.env`
- **API errors**: Check your OpenAI API key is valid and has credits
- **Slow responses**: AI generation takes 2-5 seconds depending on OpenAI API latency
- **Fallback behavior**: If AI fails, the app falls back to basic synthetic summaries

## Customization

- **Theme**: Modify `src/theme/theme.ts` for UI customization
- **Database Models**: Update `backend/src/models/db_models.py` to change schema
- **API Endpoints**: Extend `backend/src/api/main.py` for new endpoints
- **Synthetic Data**: Adjust `backend/src/etl/synthetic_data.py` to change data generation
- **AI Prompts**: Customize prompts in `backend/src/llm/` modules to change AI output style

## License

MIT
