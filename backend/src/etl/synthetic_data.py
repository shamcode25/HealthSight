import random
from datetime import datetime, timedelta
from typing import List
from ..models.db_models import PatientEpisode, SafetyIncident, DataQualityIssue


def generate_patient_names(count: int) -> List[str]:
    first_names = [
        "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
        "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
        "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
        "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
        "Steven", "Kimberly", "Andrew", "Emily", "Paul", "Donna", "Joshua", "Michelle",
    ]
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
        "Rodriguez", "Martinez", "Hernandez", "Lopez", "Wilson", "Anderson", "Thomas", "Taylor",
        "Moore", "Jackson", "Martin", "Lee", "Thompson", "White", "Harris", "Sanchez",
        "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
    ]
    
    names = []
    for _ in range(count):
        first = random.choice(first_names)
        last = random.choice(last_names)
        names.append(f"{first} {last}")
    return names


def get_risk_level(score: float) -> str:
    if score >= 0.7:
        return "High"
    elif score >= 0.4:
        return "Medium"
    else:
        return "Low"


def generate_episode_summary(episode: PatientEpisode) -> str:
    diagnoses_map = {
        "Heart Failure": f"{episode.patient_name}, {episode.primary_diagnosis}. Multiple comorbidities including diabetes and renal insufficiency. Requires close monitoring.",
        "COPD Exacerbation": f"{episode.patient_name}, severe COPD exacerbation. Responded well to treatment. Oxygen-dependent at discharge.",
        "Pneumonia": f"{episode.patient_name}, community-acquired pneumonia. Responded well to antibiotics. Fully recovered.",
        "Hip Fracture": f"{episode.patient_name}, post hip fracture repair. Stable condition, mobilizing well with assistance.",
        "Stroke": f"{episode.patient_name}, ischemic stroke. Left-sided weakness, improving with rehabilitation. Requires ongoing therapy.",
    }
    return diagnoses_map.get(episode.primary_diagnosis, f"{episode.patient_name}, {episode.primary_diagnosis}. Stable condition.")


def generate_risk_explanation(episode: PatientEpisode, risk_level: str) -> str:
    if risk_level == "High":
        return f"High readmission risk due to {episode.primary_diagnosis.lower()}, multiple comorbidities, and complex medication regimen requiring close monitoring."
    elif risk_level == "Medium":
        return f"Moderate readmission risk due to {episode.primary_diagnosis.lower()}, age factors, and potential for complications."
    else:
        return f"Low readmission risk due to good response to treatment, no underlying chronic conditions, and favorable patient factors."


def generate_next_action(episode: PatientEpisode, risk_level: str) -> str:
    if risk_level == "High":
        return f"Schedule follow-up appointment within 3-5 days. Medication compliance support. Care coordination with primary care. Home health monitoring if indicated."
    elif risk_level == "Medium":
        return f"Follow-up appointment within 7-10 days. Medication review. Patient education on condition management. Monitor for complications."
    else:
        return f"Routine follow-up in 2-4 weeks. Complete prescribed medications. Return if symptoms worsen. Standard discharge protocol."


def generate_patient_episodes(count: int = 500) -> List[PatientEpisode]:
    units = ["Cardiology", "Orthopedics", "Pulmonology", "General Medicine", "Oncology", "Neurology"]
    diagnoses = [
        "Heart Failure", "COPD Exacerbation", "Pneumonia", "Hip Fracture", "Stroke",
        "Acute Myocardial Infarction", "Diabetes Complications", "Hypertension", "Asthma",
        "Chemotherapy Complications", "Gastroenteritis", "Sepsis", "Renal Failure",
    ]
    
    names = generate_patient_names(count)
    episodes = []
    
    for i in range(count):
        episode_id = f"EP{str(i+1).zfill(6)}"
        patient_id = f"P{str(i+1).zfill(5)}"
        admit_date = datetime.now() - timedelta(days=random.randint(0, 180))
        discharge_date = None
        los = None
        
        if random.random() > 0.2:  # 80% discharged
            los = round(random.uniform(1, 15), 1)
            discharge_date = admit_date + timedelta(days=int(los))
        
        risk_score = round(random.uniform(0.1, 0.95), 3)
        risk_level = get_risk_level(risk_score)
        
        episode = PatientEpisode(
            episode_id=episode_id,
            patient_id=patient_id,
            patient_name=names[i],
            unit=random.choice(units),
            admit_date=admit_date,
            discharge_date=discharge_date,
            length_of_stay=los,
            primary_diagnosis=random.choice(diagnoses),
            readmitted_30d=random.random() < 0.15,  # 15% readmitted
            readmission_risk_score=risk_score,
        )
        
        episode.summary = generate_episode_summary(episode)
        episode.risk_explanation = generate_risk_explanation(episode, risk_level)
        episode.next_best_action = generate_next_action(episode, risk_level)
        
        episodes.append(episode)
    
    return episodes


def generate_safety_incidents(episodes: List[PatientEpisode], count: int = 200) -> List[SafetyIncident]:
    categories = ["Falls", "Medication Error", "Pressure Injury", "Infection", "Other"]
    severities = ["Low", "Medium", "High", "Critical"]
    statuses = ["Resolved", "Under Review", "Monitoring", "Active"]
    
    incidents = []
    episode_ids = [e.episode_id for e in episodes] if episodes else []
    
    for i in range(count):
        incident_id = f"SI{str(i+1).zfill(6)}"
        episode_id = random.choice(episode_ids) if episode_ids and random.random() > 0.3 else None
        
        # Get unit from episode or random
        if episode_id:
            episode = next((e for e in episodes if e.episode_id == episode_id), None)
            unit = episode.unit if episode else random.choice(["Cardiology", "Orthopedics", "Pulmonology", "General Medicine"])
        else:
            unit = random.choice(["Cardiology", "Orthopedics", "Pulmonology", "General Medicine"])
        
        category = random.choice(categories)
        severity = random.choices(severities, weights=[30, 40, 25, 5])[0]
        status = random.choice(statuses)
        
        descriptions = {
            "Falls": "Patient fall in bathroom, no injury" if severity == "Low" else "Patient fall resulting in injury",
            "Medication Error": "Wrong medication dose administered, corrected immediately" if severity == "Low" else "Serious medication error, patient monitoring required",
            "Pressure Injury": "Stage 2 pressure ulcer discovered during assessment",
            "Infection": "Hospital-acquired infection, culture pending",
            "Other": "Incident logged for review",
        }
        
        incident_date = datetime.now() - timedelta(days=random.randint(0, 60))
        
        incident = SafetyIncident(
            incident_id=incident_id,
            episode_id=episode_id,
            date=incident_date,
            unit=unit,
            category=category,
            severity=severity,
            status=status,
            description=descriptions.get(category, "Incident reported"),
        )
        
        incidents.append(incident)
    
    return incidents


def generate_data_quality_issues(episodes: List[PatientEpisode], count: int = 300) -> List[DataQualityIssue]:
    issue_types = ["Invalid", "Missing", "Duplicate", "Stale"]
    severities = ["Low", "Medium", "High"]
    units = ["Cardiology", "Orthopedics", "Pulmonology", "General Medicine", "Oncology", "Neurology"]
    fields = ["Discharge Date", "Primary Diagnosis", "Patient Record", "Last Updated", "LOS", "Discharge Disposition"]
    
    issues = []
    episode_ids = [e.episode_id for e in episodes] if episodes else []
    
    for i in range(count):
        record_id = random.choice(episode_ids) if episode_ids else f"REC{str(i+1).zfill(6)}"
        issue_type = random.choice(issue_types)
        severity = random.choices(severities, weights=[20, 50, 30])[0]
        field = random.choice(fields)
        unit = random.choice(units)
        
        descriptions = {
            "Invalid": f"{field} value is invalid or out of range",
            "Missing": f"{field} is missing or null",
            "Duplicate": f"Duplicate record detected for {field}",
            "Stale": f"Record not updated in 90+ days",
        }
        
        last_updated = datetime.now() - timedelta(days=random.randint(1, 120))
        
        issue = DataQualityIssue(
            record_type="episode",
            record_id=record_id,
            unit=unit,
            issue_type=issue_type,
            field=field,
            severity=severity,
            description=descriptions.get(issue_type, "Data quality issue detected"),
            last_updated=last_updated,
        )
        
        issues.append(issue)
    
    return issues
