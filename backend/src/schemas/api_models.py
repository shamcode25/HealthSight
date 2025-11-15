from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# Base Models
class PatientEpisodeBase(BaseModel):
    episode_id: str
    patient_id: str
    patient_name: str
    unit: str
    admit_date: datetime
    discharge_date: Optional[datetime] = None
    length_of_stay: Optional[float] = None
    primary_diagnosis: str
    readmitted_30d: bool = False
    readmission_risk_score: Optional[float] = None
    summary: Optional[str] = None
    risk_explanation: Optional[str] = None
    next_best_action: Optional[str] = None


class PatientEpisode(PatientEpisodeBase):
    id: int

    class Config:
        from_attributes = True


class SafetyIncidentBase(BaseModel):
    incident_id: str
    episode_id: Optional[str] = None
    date: datetime
    unit: str
    category: str
    severity: str
    status: str
    description: str


class SafetyIncident(SafetyIncidentBase):
    id: int

    class Config:
        from_attributes = True


class DataQualityIssueBase(BaseModel):
    record_type: str
    record_id: str
    unit: str
    issue_type: str
    field: str
    severity: str
    description: str
    last_updated: datetime


class DataQualityIssue(DataQualityIssueBase):
    id: int

    class Config:
        from_attributes = True


# Summary Schemas
class OverviewMetrics(BaseModel):
    readmissionRate: dict
    avgLOS: dict
    safetyEvents: dict
    dataQualityScore: dict


class DataQualityMetrics(BaseModel):
    invalidRecords: dict
    missingFields: dict
    duplicates: dict
    staleEpisodes: dict


class ReadmissionRiskRecord(BaseModel):
    episode: PatientEpisode
    risk_level: str
