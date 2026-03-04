from ai.ollama_client import OllamaClient
from utils.helpers import setup_logger

logger = setup_logger("MessageGenerator")

class MessageGenerator:
    def __init__(self):
        self.client = OllamaClient()

    def create_linkedin_dm(self, name: str, role: str, company: str) -> str:
        """Constructs a prompt and generates a LinkedIn message."""
        prompt = (
            f"Write a short, personalized LinkedIn message to {name}, who is a {role} "
            f"working at {company}. Introduce a potential collaboration opportunity. "
            f"Keep it professional, engaging, and under 60 words. Do not include placeholders like [Your Name], just the message content."
        )
        
        message = self.client.generate(prompt)
        
        if message:
            logger.info("Successfully generated LinkedIn message.")
            return message
        else:
            logger.warning("Failed to generate message, using fallback.")
            return f"Hi {name}, I came across your profile and saw you're working at {company} as a {role}. I'd love to connect and discuss potential synergies!"
