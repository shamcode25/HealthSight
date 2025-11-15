from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from ..config import settings


def get_llm():
    """Get configured OpenAI LLM instance"""
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not set. Please set it in your .env file.")
    
    return ChatOpenAI(
        model_name=settings.OPENAI_MODEL,
        temperature=settings.OPENAI_TEMPERATURE,
        openai_api_key=settings.OPENAI_API_KEY,
    )


def format_episode_context(episode) -> str:
    """Format patient episode data as context for LLM prompts"""
    context = f"""Patient Information:
- Patient ID: {episode.patient_id}
- Patient Name: {episode.patient_name}
- Unit: {episode.unit}
- Admission Date: {episode.admit_date.strftime('%Y-%m-%d') if episode.admit_date else 'N/A'}
- Discharge Date: {episode.discharge_date.strftime('%Y-%m-%d') if episode.discharge_date else 'Still admitted'}
- Length of Stay: {episode.length_of_stay if episode.length_of_stay else 'N/A'} days
- Primary Diagnosis: {episode.primary_diagnosis}
- Readmission Risk Score: {episode.readmission_risk_score if episode.readmission_risk_score else 'N/A'}
- Previously Readmitted (30-day): {'Yes' if episode.readmitted_30d else 'No'}
"""
    return context
