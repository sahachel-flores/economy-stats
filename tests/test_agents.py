from app.agents.selector_agent_class import SelectorAgent
from app.agents.editor_agent_class import EditorAgent
from app.agents.sentiment_analysis_agent import SentimentAnalysisAgent
from app.agents.agent_context_class import AgentContext
from sqlalchemy.ext.asyncio import AsyncSession

def test_selector_agent():
    """
    Test the selector agent.
    """
    agent = SelectorAgent("Selector Agent")
    context = AgentContext()