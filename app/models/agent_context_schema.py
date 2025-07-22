# app/models/agent_context_schema.py
from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class AgentContext(BaseModel):
    """
    This class is used to keep track of state and history of the agents.
    """
    
    # Control and loop tracking
    attempt: int = Field(default=1, description="Current attempt number")
    max_attempts: int = Field(default=5, description="Maximum allowed retry attempts")
    
    # Topic tracking
    topic: str = Field(default="US Economy", description="The topic of the news articles")

    # Articles selection
    articles: List[dict] = Field(default_factory=list, description="List of articles returned by the news api")
    
    # Article tracking
    selected_articles_ids: List[int] = Field(default_factory=list, description="Ids of selected articles by selector agent")
    selected_articles_content: List[dict] = Field(default_factory=list, description="Content of selected articles by selector agent")
    rejected_articles_ids: List[int] = Field(default_factory=list, description="Ids of Articles that were rejected by verifier")
    approved_articles_ids: List[int] = Field(default_factory=list, description="Ids of Articles approved by reviewer")
    approved_articles_content: List[dict] = Field(default_factory=list, description="Content of Articles approved by reviewer")

    # Raw responses (useful for debugging)
    #last_selector_response: Optional[str] = Field(default=None)
    #last_verifier_response: Optional[str] = Field(default=None)

    # history
    selector_history: List[dict] = Field(default_factory=list, description="History of selector agent")
    editor_history: List[dict] = Field(default_factory=list, description="History of verifier agent")

    # Full audit trail
    all_attempts_history: List[Dict[str, List[dict]]] = Field(default_factory=list, description="Tracks all attempts with article selections and feedback")

