from app.agents.selector_agent_class import SelectorAgent
from app.agents.editor_agent_class import EditorAgent
from app.agents.sentiment_analysis_agent import SentimentAnalysisAgent
from app.models.agent_context_schema import AgentContext
from app.db.session import SessionLocal

def test_selector_agent():
    """
    Test the selector agent.
    """
    agent = SelectorAgent("Selector Agent")
    context = AgentContext()