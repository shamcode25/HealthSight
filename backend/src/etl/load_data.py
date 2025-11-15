from sqlalchemy.orm import Session
from ..db import Base, engine, SessionLocal
from ..models.db_models import PatientEpisode, SafetyIncident, DataQualityIssue
from .synthetic_data import generate_patient_episodes, generate_safety_incidents, generate_data_quality_issues


def init_db():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")


def seed_database():
    """Seed the database with synthetic data if empty"""
    db = SessionLocal()
    try:
        # Check if data already exists
        episode_count = db.query(PatientEpisode).count()
        
        if episode_count > 0:
            print(f"✓ Database already contains {episode_count} episodes, skipping seed")
            return
        
        print("Seeding database with synthetic data...")
        
        # Generate and insert episodes
        print("Generating patient episodes...")
        episodes = generate_patient_episodes(count=500)
        db.add_all(episodes)
        db.commit()
        print(f"✓ Inserted {len(episodes)} patient episodes")
        
        # Generate and insert safety incidents
        print("Generating safety incidents...")
        incidents = generate_safety_incidents(episodes, count=200)
        db.add_all(incidents)
        db.commit()
        print(f"✓ Inserted {len(incidents)} safety incidents")
        
        # Generate and insert data quality issues
        print("Generating data quality issues...")
        issues = generate_data_quality_issues(episodes, count=300)
        db.add_all(issues)
        db.commit()
        print(f"✓ Inserted {len(issues)} data quality issues")
        
        print("✓ Database seeding completed successfully")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error seeding database: {e}")
        raise
    finally:
        db.close()
