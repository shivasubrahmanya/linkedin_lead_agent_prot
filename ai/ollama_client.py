import os
import requests
import json
from typing import Optional
from utils.helpers import setup_logger

logger = setup_logger("OllamaClient")

class OllamaClient:
    def __init__(self, model_name: str = "llama3"):
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model = model_name

    def generate(self, prompt: str) -> Optional[str]:
        """Send a prompt to local Ollama instance and get text response."""
        url = f"{self.host}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            logger.info(f"Sending prompt to Ollama ({self.model})...")
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            return data.get("response", "").strip()
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama generation failed: {e}")
            return None
        except json.JSONDecodeError:
            logger.error("Failed to parse JSON response from Ollama")
            return None
