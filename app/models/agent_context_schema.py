# app/models/agent_context_schema.py
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class AgentContext(BaseModel):
    # Control and loop tracking
    attempt: int = Field(default=1, description="Current attempt number")
    max_attempts: int = Field(default=5, description="Maximum allowed retry attempts")

    # Article tracking
    selected_articles: List[dict] = Field(default_factory=list, description="Current list of selected articles")
    rejected_articles: List[dict] = Field(default_factory=list, description="Articles that were rejected by verifier")
    approved_articles: List[dict] = Field(default_factory=list, description="Articles approved by reviewer")

    # Communication history with LLM
    feedback_log: List[dict] = Field(default_factory=list, description="Messages from verifier for agent improvement")

    # Raw responses (useful for debugging)
    last_selector_response: Optional[str] = Field(default=None)
    last_verifier_response: Optional[str] = Field(default=None)

    # Full audit trail
    all_attempts_history: List[Dict[str, List[dict]]] = Field(default_factory=list, description="Tracks all attempts with article selections and feedback")

    # Tool-use state (e.g., scraped articles)
    scraped_text_cache: Dict[str, str] = Field(default_factory=dict, description="Cache of scraped article text by URL")
