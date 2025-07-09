# app/agents/utils.py

import re

def detect_scrape_request(response: str) -> str | None:
    match = re.search(r"SCRAPE:\s*(https?://\S+)", response, re.IGNORECASE)
    if match:
        return match.group(1)
    return None
