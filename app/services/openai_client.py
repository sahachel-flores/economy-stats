# app/services/openai_client.py
from dotenv import load_dotenv
from app.services.logger import agent_logger as logger
from openai import OpenAI
from app.agents.agent_context_class import AgentContext

load_dotenv()
MODEL = 'gpt-4o-mini'



def ask_openai(messages: list, model: str = MODEL, temperature: float = 0.3) -> None:
    """
    Sends a prompt to OpenAI and returns the model's response as plain text.
    """
    logger.info(f"---------------------------------Entering ask_openai---------------------------------")
    openai = OpenAI()
    try:
        logger.info(f"\t\t-----------Sending request to OpenAI-----------")
        # Send the request to OpenAI
        response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
        ) 

        return response.choices[0].message.content
        
    
        
    except Exception as e:
        logger.error(f"Fatal ---> [OpenAI Error] {e}")
        return []





