from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db import Base
from datetime import datetime


class PatientEpisode(Base):
    __tablename__ = "patient_episodes"

    id = Column(Integer, primary_key=True, index=True)
    episode_id = Column(String, unique=True, index=True, nullable=False)
    patient_id = Column(String, index=True, nullable=False)
    patient_name = Column(String, nullable=False)
    unit = Column(String, nullable=False)
    admit_date = Column(DateTime, nullable=False)
    discharge_date = Column(DateTime, nullable=True)
    length_of_stay = Column(Float, nullable=True)
    primary_diagnosis = Column(String, nullable=False)
    readmitted_30d = Column(Boolean, default=False)
    readmission_risk_score = Column(Float, nullable=True)
    summary = Column(Text, nullable=True)  # Legacy field, kept for backward compatibility
    risk_explanation = Column(Text, nullable=True)  # Legacy field
    next_best_action = Column(Text, nullable=True)  # Legacy field
    # AI-generated fields
    summary_text = Column(Text, nullable=True)  # AI-generated summary
    recommendations = Column(Text, nullable=True)  # AI-generated recommendations (alternative to next_best_action)
    ai_generated_at = Column(DateTime, nullable=True)  # Timestamp when AI content was generated
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    safety_incidents = relationship("SafetyIncident", back_populates="episode", cascade="all, delete-orphan")


class SafetyIncident(Base):
    __tablename__ = "safety_incidents"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(String, unique=True, index=True, nullable=False)
    episode_id = Column(String, ForeignKey("patient_episodes.episode_id"), nullable=True)
    date = Column(DateTime, nullable=False)
    unit = Column(String, nullable=False)
    category = Column(String, nullable=False)
    severity = Column(String, nullable=False)  # Low, Medium, High, Critical
    status = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    episode = relationship("PatientEpisode", back_populates="safety_incidents")


class DataQualityIssue(Base):
    __tablename__ = "data_quality_issues"

    id = Column(Integer, primary_key=True, index=True)
    record_type = Column(String, nullable=False)  # episode, patient, etc.
    record_id = Column(String, index=True, nullable=False)
    unit = Column(String, nullable=False)
    issue_type = Column(String, nullable=False)  # Invalid, Missing, Duplicate, Stale
    field = Column(String, nullable=False)
    severity = Column(String, nullable=False)  # Low, Medium, High
    description = Column(Text, nullable=False)
    last_updated = Column(DateTime, nullable=False, server_default=func.now())
    created_at = Column(DateTime, server_default=func.now())
