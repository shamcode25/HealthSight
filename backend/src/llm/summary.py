from langchain.prompts import ChatPromptTemplate
from ..models.db_models import PatientEpisode
from .llm_utils import get_llm, format_episode_context


def generate_episode_summary(episode: PatientEpisode) -> str:
    """
    Generate a concise patient episode summary using AI.
    
    Args:
        episode: PatientEpisode database model instance
        
    Returns:
        AI-generated summary string
    """
    llm = get_llm()
    
    context = format_episode_context(episode)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a healthcare analytics assistant. Your role is to provide clear, concise summaries of patient episodes for healthcare professionals."),
        ("human", """Summarize the following patient case. Include:
1. Patient admission context and primary diagnosis
2. Length of stay if available
3. Key clinical details
4. Current status (discharged or still admitted)

Keep the summary professional, concise (2-3 sentences), and focused on the essential clinical information.

Patient Episode Data:
{context}""")
    ])
    
    chain = prompt | llm
    
    try:
        response = chain.invoke({"context": context})
        return response.content.strip()
    except Exception as e:
        # Fallback to a basic summary if AI call fails
        return f"{episode.patient_name} was admitted to {episode.unit} with {episode.primary_diagnosis}. Length of stay: {episode.length_of_stay or 'Ongoing'} days."
