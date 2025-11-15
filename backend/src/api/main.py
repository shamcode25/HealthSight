from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta
from typing import Optional
import random

from ..db import get_db, init_db
from ..etl.load_data import seed_database
from ..models.db_models import PatientEpisode, SafetyIncident, DataQualityIssue
from ..schemas.api_models import (
    PatientEpisode as PatientEpisodeSchema,
    SafetyIncident as SafetyIncidentSchema,
    DataQualityIssue as DataQualityIssueSchema,
    OverviewMetrics,
    DataQualityMetrics,
)
from ..config import settings
from ..llm.summary import generate_episode_summary
from ..llm.risk_explanation import generate_risk_explanation
from ..llm.recommendations import generate_next_best_action

app = FastAPI(title="Healthcare Analytics API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database and seed data on startup"""
    init_db()
    seed_database()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/overview-metrics")
async def get_overview_metrics(db: Session = Depends(get_db)):
    """Get overview dashboard metrics"""
    
    # Calculate readmission rate
    total_episodes = db.query(PatientEpisode).filter(
        PatientEpisode.discharge_date.isnot(None)
    ).count()
    readmitted_count = db.query(PatientEpisode).filter(
        and_(
            PatientEpisode.discharge_date.isnot(None),
            PatientEpisode.readmitted_30d == True
        )
    ).count()
    readmission_rate = round((readmitted_count / total_episodes * 100), 1) if total_episodes > 0 else 0
    
    # Calculate average length of stay
    avg_los_result = db.query(func.avg(PatientEpisode.length_of_stay)).filter(
        PatientEpisode.length_of_stay.isnot(None)
    ).scalar()
    avg_los = round(avg_los_result, 1) if avg_los_result else 0
    
    # Count safety events (last 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    safety_events_count = db.query(SafetyIncident).filter(
        SafetyIncident.date >= thirty_days_ago
    ).count()
    
    # Calculate data quality score
    total_issues = db.query(DataQualityIssue).count()
    high_severity_issues = db.query(DataQualityIssue).filter(
        DataQualityIssue.severity == "High"
    ).count()
    # Simple scoring: 100 - (high issues * 2) - (total issues * 0.1)
    quality_score = max(0, min(100, round(100 - (high_severity_issues * 2) - (total_issues * 0.1), 1)))
    
    # Determine risk levels
    def get_risk_level(rate: float, threshold_low: float = 10, threshold_high: float = 15) -> str:
        if rate >= threshold_high:
            return "High"
        elif rate >= threshold_low:
            return "Medium"
        return "Low"
    
    return {
        "readmissionRate": {
            "label": "Readmission Rate",
            "value": f"{readmission_rate}%",
            "riskLevel": get_risk_level(readmission_rate),
            "change": f"+{round(random.uniform(0.5, 2.5), 1)}%" if random.random() > 0.5 else f"-{round(random.uniform(0.5, 2.0), 1)}%",
        },
        "avgLOS": {
            "label": "Avg LOS",
            "value": str(avg_los),
            "riskLevel": get_risk_level(avg_los, threshold_low=4, threshold_high=6),
            "change": f"-{round(random.uniform(0.1, 0.5), 1)} days",
        },
        "safetyEvents": {
            "label": "Safety Events",
            "value": str(safety_events_count),
            "riskLevel": get_risk_level(safety_events_count, threshold_low=20, threshold_high=30),
            "change": f"+{random.randint(1, 5)}" if random.random() > 0.5 else f"-{random.randint(1, 3)}",
        },
        "dataQualityScore": {
            "label": "Data Quality Score",
            "value": f"{quality_score}%",
            "riskLevel": get_risk_level(100 - quality_score, threshold_low=5, threshold_high=10),
            "change": f"+{round(random.uniform(1, 3), 1)}%",
        },
    }


@app.get("/readmissions/list")
async def get_readmissions_list(
    unit: Optional[str] = Query(None, description="Filter by unit"),
    risk_level: Optional[str] = Query(None, description="Filter by risk level (Low, Medium, High)"),
    db: Session = Depends(get_db)
):
    """Get list of patient episodes with readmission risks"""
    
    query = db.query(PatientEpisode)
    
    # Apply filters
    if unit and unit != "All":
        query = query.filter(PatientEpisode.unit == unit)
    
    if risk_level and risk_level != "All":
        # Determine risk level based on score
        if risk_level == "High":
            query = query.filter(PatientEpisode.readmission_risk_score >= 0.7)
        elif risk_level == "Medium":
            query = query.filter(
                and_(
                    PatientEpisode.readmission_risk_score >= 0.4,
                    PatientEpisode.readmission_risk_score < 0.7
                )
            )
        elif risk_level == "Low":
            query = query.filter(PatientEpisode.readmission_risk_score < 0.4)
    
    episodes = query.order_by(PatientEpisode.readmission_risk_score.desc().nulls_last()).all()
    
    return [
        {
            "id": ep.episode_id,
            "patientId": ep.patient_id,
            "patientName": ep.patient_name,
            "unit": ep.unit,
            "admissionDate": ep.admit_date.isoformat(),
            "dischargeDate": ep.discharge_date.isoformat() if ep.discharge_date else None,
            "riskLevel": "High" if ep.readmission_risk_score and ep.readmission_risk_score >= 0.7 else "Medium" if ep.readmission_risk_score and ep.readmission_risk_score >= 0.4 else "Low",
            "los": ep.length_of_stay,
            "diagnosis": ep.primary_diagnosis,
            "summary": ep.summary,
            "riskExplanation": ep.risk_explanation,
            "nextBestAction": ep.next_best_action,
        }
        for ep in episodes
    ]


@app.get("/readmissions/high-risk")
async def get_high_risk_readmissions(db: Session = Depends(get_db)):
    """Get high-risk readmission episodes"""
    
    episodes = db.query(PatientEpisode).filter(
        PatientEpisode.readmission_risk_score >= 0.7
    ).order_by(PatientEpisode.readmission_risk_score.desc()).limit(20).all()
    
    return [
        {
            "id": ep.episode_id,
            "patientId": ep.patient_id,
            "patientName": ep.patient_name,
            "unit": ep.unit,
            "admissionDate": ep.admit_date.isoformat(),
            "dischargeDate": ep.discharge_date.isoformat() if ep.discharge_date else None,
            "riskLevel": "High",
            "los": ep.length_of_stay,
            "diagnosis": ep.primary_diagnosis,
            "summary": ep.summary,
            "riskExplanation": ep.risk_explanation,
            "nextBestAction": ep.next_best_action,
        }
        for ep in episodes
    ]


@app.get("/readmissions/{episode_id}")
async def get_episode_by_id(episode_id: str, db: Session = Depends(get_db)):
    """Get a specific episode by ID"""
    
    episode = db.query(PatientEpisode).filter(
        PatientEpisode.episode_id == episode_id
    ).first()
    
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    
    risk_score = episode.readmission_risk_score or 0
    risk_level = "High" if risk_score >= 0.7 else "Medium" if risk_score >= 0.4 else "Low"
    
    return {
        "id": episode.episode_id,
        "patientId": episode.patient_id,
        "patientName": episode.patient_name,
        "unit": episode.unit,
        "admissionDate": episode.admit_date.isoformat(),
        "dischargeDate": episode.discharge_date.isoformat() if episode.discharge_date else None,
        "riskLevel": risk_level,
        "los": episode.length_of_stay,
        "diagnosis": episode.primary_diagnosis,
        "summary": episode.summary_text or episode.summary,  # Prefer AI-generated summary
        "summary_text": episode.summary_text,
        "riskExplanation": episode.risk_explanation,
        "nextBestAction": episode.recommendations or episode.next_best_action,  # Prefer AI-generated recommendations
        "recommendations": episode.recommendations,
    }


@app.get("/quality/incidents")
async def get_safety_incidents(db: Session = Depends(get_db)):
    """Get safety incidents"""
    
    incidents = db.query(SafetyIncident).order_by(SafetyIncident.date.desc()).all()
    
    return [
        {
            "id": inc.incident_id,
            "date": inc.date.isoformat(),
            "category": inc.category,
            "severity": inc.severity,
            "description": inc.description,
            "unit": inc.unit,
            "status": inc.status,
        }
        for inc in incidents
    ]


@app.get("/quality/incidents/summary")
async def get_safety_incidents_summary(db: Session = Depends(get_db)):
    """Get safety incidents summary and KPIs"""
    
    thirty_days_ago = datetime.now() - timedelta(days=30)
    
    # Count by category
    falls_count = db.query(SafetyIncident).filter(
        and_(
            SafetyIncident.category == "Falls",
            SafetyIncident.date >= thirty_days_ago
        )
    ).count()
    
    med_errors_count = db.query(SafetyIncident).filter(
        and_(
            SafetyIncident.category == "Medication Error",
            SafetyIncident.date >= thirty_days_ago
        )
    ).count()
    
    total_incidents = db.query(SafetyIncident).filter(
        SafetyIncident.date >= thirty_days_ago
    ).count()
    
    # Category distribution for pie chart
    categories = db.query(
        SafetyIncident.category,
        func.count(SafetyIncident.id).label("count")
    ).filter(
        SafetyIncident.date >= thirty_days_ago
    ).group_by(SafetyIncident.category).all()
    
    return {
        "kpis": {
            "falls": {
                "label": "Falls",
                "value": str(falls_count),
                "riskLevel": "Medium" if falls_count > 5 else "Low",
                "change": f"+{random.randint(1, 3)}" if random.random() > 0.5 else f"-{random.randint(0, 2)}",
            },
            "medErrors": {
                "label": "Med Errors",
                "value": str(med_errors_count),
                "riskLevel": "Low" if med_errors_count < 3 else "Medium",
                "change": f"-{random.randint(0, 2)}" if random.random() > 0.7 else f"+{random.randint(0, 2)}",
            },
            "incidents": {
                "label": "Total Incidents",
                "value": str(total_incidents),
                "riskLevel": "Medium" if total_incidents > 15 else "Low",
                "change": f"+{random.randint(1, 4)}" if random.random() > 0.5 else f"-{random.randint(1, 3)}",
            },
        },
        "categoryData": [
            {"name": cat, "value": count, "fill": "#ef4444" if cat == "Falls" else "#f59e0b" if cat == "Medication Error" else "#8b5cf6" if cat == "Pressure Injury" else "#3b82f6" if cat == "Infection" else "#6b7280"}
            for cat, count in categories
        ],
    }


@app.get("/data-quality/issues")
async def get_data_quality_issues(db: Session = Depends(get_db)):
    """Get data quality issues"""
    
    issues = db.query(DataQualityIssue).order_by(
        func.case(
            (DataQualityIssue.severity == "High", 1),
            (DataQualityIssue.severity == "Medium", 2),
            (DataQualityIssue.severity == "Low", 3),
            else_=4
        ),
        DataQualityIssue.last_updated.desc()
    ).all()
    
    return [
        {
            "id": f"DQ{str(iss.id).zfill(6)}",
            "recordId": iss.record_id,
            "unit": iss.unit,
            "issueType": iss.issue_type,
            "field": iss.field,
            "description": iss.description,
            "severity": iss.severity,
            "lastUpdated": iss.last_updated.isoformat(),
        }
        for iss in issues
    ]


@app.get("/data-quality/metrics")
async def get_data_quality_metrics(db: Session = Depends(get_db)):
    """Get data quality metrics and KPIs"""
    
    # Count by issue type
    invalid_count = db.query(DataQualityIssue).filter(
        DataQualityIssue.issue_type == "Invalid"
    ).count()
    
    missing_count = db.query(DataQualityIssue).filter(
        DataQualityIssue.issue_type == "Missing"
    ).count()
    
    duplicate_count = db.query(DataQualityIssue).filter(
        DataQualityIssue.issue_type == "Duplicate"
    ).count()
    
    stale_count = db.query(DataQualityIssue).filter(
        DataQualityIssue.issue_type == "Stale"
    ).count()
    
    # Count by unit for chart
    unit_stats = db.query(
        DataQualityIssue.unit,
        func.sum(func.case((DataQualityIssue.issue_type == "Invalid", 1), else_=0)).label("invalid"),
        func.sum(func.case((DataQualityIssue.issue_type == "Missing", 1), else_=0)).label("missing"),
        func.sum(func.case((DataQualityIssue.issue_type == "Duplicate", 1), else_=0)).label("duplicates"),
        func.sum(func.case((DataQualityIssue.issue_type == "Stale", 1), else_=0)).label("stale"),
    ).group_by(DataQualityIssue.unit).all()
    
    return {
        "kpis": {
            "invalidRecords": {
                "label": "Invalid Records",
                "value": str(invalid_count),
                "riskLevel": "Medium" if invalid_count > 100 else "Low",
                "change": f"-{random.randint(5, 15)}" if random.random() > 0.5 else f"+{random.randint(2, 10)}",
            },
            "missingFields": {
                "label": "Missing Fields",
                "value": str(missing_count),
                "riskLevel": "Low" if missing_count < 100 else "Medium",
                "change": f"-{random.randint(3, 10)}" if random.random() > 0.6 else f"+{random.randint(2, 8)}",
            },
            "duplicates": {
                "label": "Duplicates",
                "value": str(duplicate_count),
                "riskLevel": "Low" if duplicate_count < 50 else "Medium",
                "change": f"-{random.randint(2, 8)}" if random.random() > 0.6 else f"+{random.randint(1, 5)}",
            },
            "staleEpisodes": {
                "label": "Stale Episodes",
                "value": str(stale_count),
                "riskLevel": "Medium" if stale_count > 50 else "Low",
                "change": f"+{random.randint(1, 5)}" if random.random() > 0.5 else f"-{random.randint(1, 4)}",
            },
        },
        "byUnit": [
            {
                "name": unit,
                "invalid": int(inv or 0),
                "missing": int(miss or 0),
                "duplicates": int(dup or 0),
                "stale": int(stale or 0),
            }
            for unit, inv, miss, dup, stale in unit_stats
        ],
    }


@app.get("/risk-distribution")
async def get_risk_distribution(db: Session = Depends(get_db)):
    """Get risk level distribution for overview page"""
    
    total = db.query(PatientEpisode).count()
    
    high_count = db.query(PatientEpisode).filter(
        PatientEpisode.readmission_risk_score >= 0.7
    ).count()
    
    medium_count = db.query(PatientEpisode).filter(
        and_(
            PatientEpisode.readmission_risk_score >= 0.4,
            PatientEpisode.readmission_risk_score < 0.7
        )
    ).count()
    
    low_count = db.query(PatientEpisode).filter(
        or_(
            PatientEpisode.readmission_risk_score < 0.4,
            PatientEpisode.readmission_risk_score.is_(None)
        )
    ).count()
    
    return [
        {"name": "Low", "value": low_count, "color": "#10b981"},
        {"name": "Medium", "value": medium_count, "color": "#f59e0b"},
        {"name": "High", "value": high_count, "color": "#ef4444"},
    ]


@app.get("/health-trends")
async def get_health_trends(db: Session = Depends(get_db)):
    """Get health trends data for overview page"""
    
    # Get last 6 months of data
    six_months_ago = datetime.now() - timedelta(days=180)
    
    # Aggregate by month
    trends = db.query(
        func.strftime("%Y-%m", PatientEpisode.admit_date).label("month"),
        func.count(PatientEpisode.id).label("episodes"),
        func.sum(func.case((PatientEpisode.readmitted_30d == True, 1), else_=0)).label("readmissions"),
    ).filter(
        PatientEpisode.admit_date >= six_months_ago
    ).group_by("month").order_by("month").all()
    
    # Format for frontend
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    
    return [
        {
            "name": month_names[i % len(month_names)],
            "readmissions": int(readmissions or 0),
            "episodes": int(episodes or 0),
        }
        for i, (month, episodes, readmissions) in enumerate(trends[-6:])  # Last 6 months
    ]


# ==================== AI Endpoints ====================

@app.post("/llm/summary/{episode_id}")
async def generate_summary(episode_id: str, db: Session = Depends(get_db)):
    """Generate AI summary for a patient episode"""
    
    episode = db.query(PatientEpisode).filter(
        PatientEpisode.episode_id == episode_id
    ).first()
    
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    
    try:
        # Generate summary using AI
        summary_text = generate_episode_summary(episode)
        
        # Save to database
        episode.summary_text = summary_text
        episode.summary = summary_text  # Also update legacy field
        episode.ai_generated_at = datetime.now()
        db.commit()
        db.refresh(episode)
        
        return {
            "episode_id": episode_id,
            "summary": summary_text,
            "generated_at": episode.ai_generated_at.isoformat() if episode.ai_generated_at else None
        }
    except ValueError as e:
        # OpenAI API key not set
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")


@app.post("/llm/risk-explanation/{episode_id}")
async def generate_risk_explanation_endpoint(episode_id: str, db: Session = Depends(get_db)):
    """Generate AI risk explanation for a patient episode"""
    
    episode = db.query(PatientEpisode).filter(
        PatientEpisode.episode_id == episode_id
    ).first()
    
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    
    try:
        # Generate risk explanation using AI
        explanation = generate_risk_explanation(episode)
        
        # Save to database
        episode.risk_explanation = explanation
        episode.ai_generated_at = datetime.now()
        db.commit()
        db.refresh(episode)
        
        return {
            "episode_id": episode_id,
            "risk_explanation": explanation,
            "generated_at": episode.ai_generated_at.isoformat() if episode.ai_generated_at else None
        }
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error generating risk explanation: {str(e)}")


@app.post("/llm/recommendations/{episode_id}")
async def generate_recommendations_endpoint(episode_id: str, db: Session = Depends(get_db)):
    """Generate AI recommendations for a patient episode"""
    
    episode = db.query(PatientEpisode).filter(
        PatientEpisode.episode_id == episode_id
    ).first()
    
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    
    try:
        # Generate recommendations using AI
        recommendations = generate_next_best_action(episode)
        
        # Save to database
        episode.recommendations = recommendations
        episode.next_best_action = recommendations  # Also update legacy field
        episode.ai_generated_at = datetime.now()
        db.commit()
        db.refresh(episode)
        
        return {
            "episode_id": episode_id,
            "recommendations": recommendations,
            "generated_at": episode.ai_generated_at.isoformat() if episode.ai_generated_at else None
        }
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")


@app.post("/llm/generate-all/{episode_id}")
async def generate_all_insights(episode_id: str, db: Session = Depends(get_db)):
    """Generate all AI insights (summary, risk explanation, recommendations) for a patient episode"""
    
    episode = db.query(PatientEpisode).filter(
        PatientEpisode.episode_id == episode_id
    ).first()
    
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    
    try:
        # Generate all AI insights
        summary_text = generate_episode_summary(episode)
        explanation = generate_risk_explanation(episode)
        recommendations = generate_next_best_action(episode)
        
        # Save all to database
        episode.summary_text = summary_text
        episode.summary = summary_text  # Legacy field
        episode.risk_explanation = explanation
        episode.recommendations = recommendations
        episode.next_best_action = recommendations  # Legacy field
        episode.ai_generated_at = datetime.now()
        db.commit()
        db.refresh(episode)
        
        return {
            "episode_id": episode_id,
            "summary": summary_text,
            "risk_explanation": explanation,
            "recommendations": recommendations,
            "generated_at": episode.ai_generated_at.isoformat() if episode.ai_generated_at else None
        }
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error generating insights: {str(e)}")


