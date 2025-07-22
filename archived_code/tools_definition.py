# app/services/tools_definition.py
# scrape tool definition
scrape_tool = {
    "type": "function",
    "function": {
        "name": "get_article_text",
        "description": "Scrape and return the full text content from the given article URL.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The full description of the article to scrape",
                    "url": "List of URLs of the article to scrape"
                }
            },
            "required": ["url"]
        }
    }
}
