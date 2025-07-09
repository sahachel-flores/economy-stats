# app/services/logger.py

import logging
import os
from logging.handlers import TimedRotatingFileHandler

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def create_logger(name: str, filename: str, level=logging.INFO, when="midnight", backup_count=7) -> logging.Logger:
    """
    Creates a rotating logger that:
    - Writes to logs/{filename}
    - Rotates every 'when' interval
    - Keeps up to backup_count old logs
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.hasHandlers():
        # Console output (during dev)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # File rotation handler
        file_handler = TimedRotatingFileHandler(
            filename=f"{LOG_DIR}/{filename}",
            when=when,               # e.g., "midnight", "D", "H"
            interval=1,
            backupCount=backup_count,
            encoding="utf-8"
        )
        file_handler.setLevel(level)

        # Formatter
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    logger.propagate = False
    return logger

# Main loggers
agent_logger = create_logger("agent-logger", "agents.log")
api_logger = create_logger("api-logger", "api.log")
