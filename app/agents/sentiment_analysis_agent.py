from app.agents.base_agent import BaseAgent
from app.agents.agent_context_class import AgentContext
from app.services.openai_client import ask_openai
from app.services.logger import agent_logger as logger
from app.services.db_tools import get_articles_using_ids_from_db
from app.schemas.agents import SentimentAnalysisResult

import ast
import json
import re
from typing import Any

class SentimentAnalysisAgent(BaseAgent):
    """
    Agent responsible for analyzing the sentiment of the articles.
    """
    def __init__(self, name: str = "Sentiment Analysis Agent", max_retries: int = 2):
        super().__init__(name, max_retries)
        self.llm_client = ask_openai
        self.article_fetcher = get_articles_using_ids_from_db
        self.logger = logger
    
    @staticmethod
    def _extract_bracket_payload(text: str) -> str:
        """
        Extract the first top-level JSON/Python list payload from LLM output.
        Handles common patterns like fenced code blocks (```python ... ```).
        """
        if not text:
            raise ValueError("Empty LLM response")

        # Prefer fenced blocks if present
        fenced = re.search(r"```(?:\w+)?\s*([\s\S]*?)\s*```", text)
        candidate = fenced.group(1) if fenced else text

        start = candidate.find("[")
        end = candidate.rfind("]")
        if start == -1 or end == -1 or end <= start:
            raise ValueError("No bracketed list payload found in LLM response")

        return candidate[start : end + 1].strip()

    @classmethod
    def parse_sentiment_analysis_response(cls, text: str) -> list[SentimentAnalysisResult]:
        payload = cls._extract_bracket_payload(text)

        data: Any
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            # Fallback for python-ish lists (single quotes, trailing commas, etc.)
            data = ast.literal_eval(payload)

        if not isinstance(data, list):
            raise ValueError(f"Expected a list, got {type(data).__name__}")

        results: list[SentimentAnalysisResult] = []
        for item in data:
            if not isinstance(item, dict):
                raise ValueError(f"Expected dict items, got {type(item).__name__}")
            results.append(SentimentAnalysisResult(**item))
        return results

    def execute(self, context: AgentContext, *args, **kwargs) -> None:
        """
        Agent for analyzing the sentiment of the articles.
        """
        try:
            logger.info(f"---------------->Executing sentiment analysis agent...")
            instruction = self.generate_input_message(context)
            message = {"role": "system", "content": instruction}
            context.agent_communication.sentiment_analysis.history.append(message)
            result = self.llm_client(context.agent_communication.sentiment_analysis.history)
            if not result:
                raise Exception("Sentiment analysis agent: Error ask_openai function failed to return a result")
            context.agent_communication.sentiment_analysis.history.append({'role': 'assistant', 'content': result}) 
            context.agent_communication.sentiment_analysis.last_response = result

            parsed = self.parse_sentiment_analysis_response(result)
            logger.info(f"Sentiment analysis agent: parsed: {parsed}")
            context.article_flow.sentiment_analysis_results = parsed
 
        except Exception as e:
            logger.error(f"Error in sentiment analysis agent: {e}")
            return None
    
    def generate_input_message(self, context: AgentContext, *args, **kwargs) -> str:
        """
        Generate the input message for the sentiment analysis agent.
        """
        instruction = f"""
        You are an expert news analyst. You will be given a list of objects which contains information about the news articles in the following structure:
        [{{
            "id": The id of the article,
            "author": The author of the article,
            "title": The title of the article,
            "description": The description of the article,
            "url": The url of the article,
            "url_to_image": The url to the image of the article,
            "published_at": The date and time the article was published,
            "content": The content of the article.
        }}]

        Instructions:
        1. Analyze the content of each article and determine the sentiment of the article.
        2. Using a scale of 1 to 100, where 1 is the most negative and 100 is the most positive, rate the article.
        3. Return a python list of objects with the following structure:
        [{{
            "id": The id of the article,
            "rating": integer value between 1 and 100,
            "sentiment": "A brief description (35-75 words) explaining the sentiment of the article."
        }}]
        4. Example output:
        [
            {{
                "id": 1,
                "rating": 50,
                "sentiment": "The article presents optimistic economic indicators with cautious undertones about potential challenges..."
            }},
            {{
                "id": 2,
                "rating": 75,
                "sentiment": "The article highlights positive economic indicators with cautious undertones about potential challenges..."
            }},
            {{
                "id": 3,
                "rating": 25,
                "sentiment": "The article presents a negative outlook on the economy with a focus on potential risks and challenges..."
            }}
        ]
        5. The number of output objects must be equal to the number of input objects.

        List of news articles:\n
        {context.article_flow.approved_articles_content}
        """
        return instruction