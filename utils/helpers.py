import logging
from typing import List
from utils.regex_patterns import EMAIL_PATTERN, WHITESPACE_PATTERN

def setup_logger(name: str) -> logging.Logger:
    """Setup a basic logger for the agent."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

def clean_text(text: str) -> str:
    """Remove extra whitespaces from text."""
    if not text:
        return ""
    return WHITESPACE_PATTERN.sub(" ", text).strip()

def extract_emails_from_text(text: str) -> List[str]:
    """Find all unique emails in a given text."""
    if not text:
        return []
    emails = EMAIL_PATTERN.findall(text)
    # Return unique emails only, lowercased
    return list(set([email.lower() for email in emails]))
