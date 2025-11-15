from langchain.prompts import ChatPromptTemplate
from ..models.db_models import PatientEpisode
from .llm_utils import get_llm, format_episode_context


def generate_risk_explanation(episode: PatientEpisode) -> str:
    """
    Generate an explanation for why a patient is at risk of 30-day readmission.
    
    Args:
        episode: PatientEpisode database model instance
        
    Returns:
        AI-generated risk explanation string
    """
    llm = get_llm()
    
    context = format_episode_context(episode)
    
    # Determine risk level
    risk_score = episode.readmission_risk_score or 0
    if risk_score >= 0.7:
        risk_level = "High"
    elif risk_score >= 0.4:
        risk_level = "Medium"
    else:
        risk_level = "Low"
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a healthcare analytics assistant specializing in readmission risk assessment. Use a professional, clinical tone suitable for healthcare professionals."),
        ("human", """Explain why this patient is at risk of 30-day readmission. The patient has a {risk_level} risk level (risk score: {risk_score}).

Consider factors such as:
- Primary diagnosis and its complexity
- Length of stay patterns
- Previous readmission history
- Patient demographics and clinical characteristics
- Condition-specific risk factors

Provide a clear, evidence-based explanation (3-4 sentences) that would be useful for care planning.

Patient Episode Data:
{context}

Risk Explanation:""")
    ])
    
    chain = prompt | llm
    
    try:
        response = chain.invoke({
            "context": context,
            "risk_level": risk_level,
            "risk_score": f"{risk_score:.2f}"
        })
        return response.content.strip()
    except Exception as e:
        # Fallback explanation if AI call fails
        return f"This patient has a {risk_level} readmission risk (score: {risk_score:.2f}) based on their {episode.primary_diagnosis} diagnosis, length of stay, and clinical characteristics. Close monitoring and follow-up care are recommended to prevent readmission."
