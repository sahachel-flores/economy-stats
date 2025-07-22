# app/services/anthropic_client.py

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()  # Ensure it loads CLAUDE_API_KEY from .env

anthropic = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
MODEL="claude-3-7-sonnet-latest"

def ask_claude(prompt: str, model: str = MODEL, temperature: float = 0.3, max_tokens: int = 512) -> str:
    """
    Sends a prompt to Claude and returns the model's response as plain text.
    """
    try:
        message = anthropic.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text.strip()
    except Exception as e:
        print(f"[Claude Error] {e}")
        return "Error: Claude failed to respond."
