from langchain.prompts import ChatPromptTemplate
from ..models.db_models import PatientEpisode
from .llm_utils import get_llm, format_episode_context


def generate_next_best_action(episode: PatientEpisode) -> str:
    """
    Generate actionable next steps to reduce readmission risk.
    
    Args:
        episode: PatientEpisode database model instance
        
    Returns:
        AI-generated recommendations string
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
        ("system", "You are a healthcare analytics assistant providing evidence-based recommendations for care transitions and readmission prevention."),
        ("human", """Provide 3 actionable next steps for this patient to reduce their risk of 30-day readmission. The patient has a {risk_level} risk level (risk score: {risk_score}).

Focus on:
1. Immediate post-discharge actions
2. Follow-up care coordination
3. Patient education or support services
4. Medication management
5. Specialist referrals if needed

Format as a numbered list (3 items). Each recommendation should be specific, actionable, and tailored to the patient's condition.

Patient Episode Data:
{context}

Recommendations:""")
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
        # Fallback recommendations if AI call fails
        fallback = f"1. Schedule follow-up appointment within 7-10 days for {episode.primary_diagnosis} monitoring.\n"
        fallback += f"2. Ensure patient education on condition management and medication compliance.\n"
        fallback += f"3. Coordinate with primary care provider for ongoing care management."
        return fallback
