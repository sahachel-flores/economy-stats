# app/services/utils.py

import json
from typing import Any
from app.services.logger import agent_logger as logger

def safe_json_parse(raw_text: str) -> Any:
    """
    Attempts to parse a string into JSON. Logs errors gracefully.
    
    Args:
        raw_text (str): The string to parse (typically from an LLM).
    
    Returns:
        Parsed JSON object (list, dict, etc.), or None if parsing fails.
    """
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as e:
        logger.error(f"[safe_json_parse] JSON decoding failed:\n{e}\nContent:\n{raw_text}")
        return None
