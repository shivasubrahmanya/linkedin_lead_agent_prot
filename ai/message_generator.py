from ai.ollama_client import OllamaClient
from utils.helpers import setup_logger

logger = setup_logger("MessageGenerator")

class MessageGenerator:
    def __init__(self):
        self.client = OllamaClient()

    def create_outreach_email(self, name: str, role: str, company: str) -> dict:
        """Constructs a professional outreach email."""
        prompt = (
            f"Write a professional outreach email to {name}, who is a {role} at {company}. "
            "The goal is to introduce a potential collaboration or partnership. "
            "The email should have a clear, engaging subject line and a professional body. "
            "Keep it concise and personalized. "
            "Return the response in the format: \nSubject: [Subject]\n\nBody: [Body]\n"
            "Do not include placeholders like [Your Name], just the content."
        )
        
        response = self.client.generate(prompt)
        
        if response and "Subject:" in response and "Body:" in response:
            parts = response.split("Body:", 1)
            subject = parts[0].replace("Subject:", "").strip()
            body = parts[1].strip()
            return {"subject": subject, "body": body}
        else:
            logger.warning("Failed to generate custom email, using fallback.")
            return {
                "subject": f"Collaboration Opportunity - {company}",
                "body": f"Hi {name},\n\nI hope this email finds you well. I came across your profile and was impressed by your work as {role} at {company}. I'm reaching out to discuss a potential collaboration that could be mutually beneficial. Would you be open to a brief chat next week?\n\nBest regards,"
            }

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
