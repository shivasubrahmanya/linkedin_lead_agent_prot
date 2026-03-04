import re

# Standard email extraction pattern
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

# Basic phone number pattern (international format or standard US)
PHONE_PATTERN = re.compile(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}")

# LinkedIn URL pattern
LINKEDIN_URL_PATTERN = re.compile(r"(https?://)?(www\.)?linkedin\.com/in/([a-zA-Z0-9_-]+)/?")

# Clean text: remove extra whitespaces
WHITESPACE_PATTERN = re.compile(r"\s+")
