# app/services/openai_client.py
import os
from dotenv import load_dotenv
import json
from app.services.logger import agent_logger as logger
from app.services.json_parser import safe_json_parse
from openai import OpenAI
from app.models.agent_context_schema import AgentContext
from app.services.article_tools import get_articles_from_ids
import ast
load_dotenv()
MODEL = 'gpt-4o-mini'

get_article_text_tool = {
    "name": "get_article_text",
    "description": "Get the full content of the article from the given article URL.",
    "parameters": {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "The full content  of the article.",
                "url": "List of URLs of the article"
            }
        },
        "required": ["url"],
        "additionalProperties": False
    }
    
}



def ask_openai(messages: list[dict], context: AgentContext, model: str = MODEL, temperature: float = 0.3) -> None:
    """
    Sends a prompt to OpenAI and returns the model's response as plain text.
    """
    logger.info(f"---------------------------------Entering ask_openai---------------------------------")
    openai = OpenAI()
    history = context.feedback_log
    content = ""
    # If history is provided, use it
    if len(history) > 0:
        logger.info(f"-----------------------Adding history to messages---------------------------")
        messages += history

    try:
        logger.info(f"\t\t-----------Sending request to OpenAI-----------")
        # List of tools to use
        tools = [{"type": "function", "function": get_article_text_tool}]
        # Send the request to OpenAI
        response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=512
        ) 

        # Get the reply from the model
        #message = response.choices[0].message
        #logger.info(f"The reply from OpenAI is: {reply}\n\n")


        # If the reply contains a tool call, convert the article text to json
        # if response.choices[0].finish_reason == "tool_calls":
            
        #     logger.info(f"Calling a tool")
            
        #     # Get the tool call
        #     tool_call = message.tool_calls[0]
        #     args = json.loads(tool_call.function.arguments)
        #     url = args.get("url")
        #     text = get_article_text(url)
        #     reply = {
        #         "role": "tool",
        #         "content": {"url": url, "text": text},
        #         "tool_call_id": tool_call.id
        #     }
        #     #logger.info(f"The return Content by OpenAI (reply) is: {reply['content']}")
        #     messages.append(reply)

        #     #adding selected articles to context
        #     for article in reply['content']:
        #         context.selected_articles.append(article)
            
        #     return
        # else:
        content = response.choices[0].message.content
        logger.info(f"The return Content by OpenAI is: \n\n{content}\n\n")
        result = ast.literal_eval(content)
        context.selected_articles = get_articles_from_ids(result)
        
    except Exception as e:
        logger.error(f"[OpenAI Error] {e}")
        return []






