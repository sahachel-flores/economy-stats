from app.agents.base_agent import BaseAgent
from app.agents.agent_context_class import AgentContext
from app.services.openai_client import ask_openai
from app.services.logger import agent_logger as logger

class SentimentAnalysisAgent(BaseAgent):
    """
    Agent responsible for analyzing the sentiment of the articles.
    """
    def __init__(self, name: str = "Sentiment Analysis Agent", max_retries: int = 2):
        super().__init__(name, max_retries)
    
    def execute(self, context: AgentContext, *args, **kwargs) -> bool:
        """
        Agent for analyzing the sentiment of the articles.
        """
        try:
            instruction = self.generate_input_message(context)
            message = {"role": "system", "content": instruction}
            context.agent_states.sentiment_analysis.history.append(message)
            result = ask_openai(context.agent_states.sentiment_analysis.history)
            parsed_result = self.parse_response(result, context)
            return parsed_result
        except Exception as e:
            logger.error(f"Error in sentiment analysis agent: {e}")
            return False
    
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