# app/models/agent_context_schema.py
from pydantic import BaseModel, Field
from typing import List, Dict, Optional



class PipelineControl(BaseModel):
    """
    Read-only configuration data that agents use for coordination
    """
    attempt: int = Field(default=1, description="Current pipeline attempt")
    max_attempts: int = Field(default=3, description="Maximum retry attempts")
    topic: str = Field(default="US Economy", description="News topic to focus on")
    target_articles: int = Field(default=5, description="Target number of approved articles")
    obtained_articles_from_news_api: int = Field(default=0, description="Number of articles obtained from News API")
    from_date: str = Field(default="2025-06-17", description="Article date range start")
    to_date: str = Field(default="2025-06-17", description="Article date range end")
    max_tokens: int = Field(default=128000, description="Maximum number of tokens for the pipeline")

class ArticleFlow(BaseModel):
    """
    Articles at different stages of the pipeline
    """
    raw_articles: List[dict] = Field(default_factory=list, description="Original articles from News API")
    articles_from_db: List[dict] = Field(default_factory=list, description="Articles from the database")
    selected_articles_ids: List[int] = Field(default_factory=list, description="IDs selected by selector agent")
    selected_articles_content: List[dict] = Field(default_factory=list, description="Full content of selected articles")
    approved_articles_ids: List[int] = Field(default_factory=list, description="IDs approved by editor agent")
    approved_articles_content: List[dict] = Field(default_factory=list, description="Full content of approved articles")
    rejected_articles_ids: List[int] = Field(default_factory=list, description="IDs rejected by editor agent")
    rejected_articles_content: List[dict] = Field(default_factory=list, description="Full content of rejected articles")
    

class SelectorState(BaseModel):
    history: List[dict] = Field(default_factory=list, description="OpenAI conversation history")
    execution_count: int = Field(default=0, description="Number of times executed")
    last_response: Optional[str] = Field(default=None, description="Last raw OpenAI response")
    attempt: int = Field(default=1, description="Selector agent attempt")
    max_attempts: int = Field(default=2, description="Maximum number of attempts to use selector agent")
    feedback: str = Field(default=None, description="Feedback from user")

class EditorState(BaseModel):
    history: List[dict] = Field(default_factory=list, description="OpenAI conversation history") 
    execution_count: int = Field(default=0, description="Number of times executed")
    last_response: Optional[str] = Field(default=None, description="Last raw OpenAI response")
    attempt: int = Field(default=1, description="Editor agent attempt")
    max_attempts: int = Field(default=2, description="Maximum number of attempts to use editor agent")
    feedback: str = Field(default=None, description="Feedback from user")

class SentimentAnalysisState(BaseModel):
    history: List[dict] = Field(default_factory=list, description="OpenAI conversation history")
    execution_count: int = Field(default=0, description="Number of times executed")
    last_response: Optional[str] = Field(default=None, description="Last raw OpenAI response")

class AgentStates(BaseModel):
    """
    Internal state for each agent - don't cross-contaminate
    """
    selector: SelectorState = Field(default_factory=lambda: SelectorState())
    editor: EditorState = Field(default_factory=lambda: EditorState())
    history: List[dict] = Field(default_factory=list, description="OpenAI conversation history")
    # Future agents will add their state here


class PipelineResults(BaseModel):
    """Final results and performance metrics"""
    success: bool = Field(default=False, description="Whether pipeline achieved target")
    total_execution_time: float = Field(default=0.0, description="Total time in seconds")
    articles_processed: int = Field(default=0, description="Total articles analyzed")
    final_approved_count: int = Field(default=0, description="Final number of approved articles")
    
    # Performance tracking
    agent_performance: Dict[str, dict] = Field(default_factory=dict, description="Per-agent metrics")
    
class AgentContext(BaseModel):
    """
    This class is used to keep track of state and history of the agents.
    """
    control: PipelineControl = Field(default_factory=PipelineControl)
    article_flow: ArticleFlow = Field(default_factory=ArticleFlow)
    agent_states: AgentStates = Field(default_factory=AgentStates)
    results: PipelineResults = Field(default_factory=PipelineResults)

    def should_continue(self) -> bool:
        """
        Check if the pipeline should continue.
        """
        return self.control.attempt <= self.control.max_attempts and len(self.article_flow.approved_articles_ids) < self.control.target_articles