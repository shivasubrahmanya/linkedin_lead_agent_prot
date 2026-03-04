import os
import requests
from dotenv import load_dotenv

# Import services
from services.google_search_service import GoogleSearchService
from services.clearbit_service import ClearbitService
from services.lusha_service import LushaService
from services.email_verifier_service import EmailVerifierService
from ai.ollama_client import OllamaClient

load_dotenv()

def check_google_search():
    print("\n--- Checking Google Search (SerpAPI) ---")
    service = GoogleSearchService()
    if not service.api_key:
        print("❌ SERPAPI_KEY is missing!")
        return
    results = service.search("test", num_results=1)
    if results:
        print("✅ Google Search is working!")
    else:
        print("❌ Google Search returned no results.")

def check_clearbit():
    print("\n--- Checking Clearbit ---")
    service = ClearbitService()
    if not service.api_key or "your_" in service.api_key:
        print("⚠️ CLEARBIT_API_KEY is a placeholder.")
    else:
        print(f"Token found: {service.api_key[:5]}...")

def check_lusha():
    print("\n--- Checking Lusha ---")
    service = LushaService()
    if not service.api_key or "your_" in service.api_key:
        print("⚠️ LUSHA_API_KEY is a placeholder.")
    else:
        print(f"Token found: {service.api_key[:5]}...")

def check_email_verifier():
    print("\n--- Checking Email Verifier ---")
    service = EmailVerifierService()
    if not service.api_key or "your_" in service.api_key:
        print("⚠️ VERIFICATION_API_KEY is a placeholder.")
    else:
        print(f"Token found: {service.api_key[:5]}...")

def check_ollama():
    print("\n--- Checking Ollama ---")
    client = OllamaClient()
    try:
        response = requests.get(f"{client.host}/api/tags", timeout=5)
        if response.status_code == 200:
            models = [m['name'] for m in response.json().get('models', [])]
            print(f"✅ Ollama is running at {client.host}")
            print(f"Available models: {models}")
            if "llama3" in models:
                print("✅ 'llama3' model is available.")
            else:
                print("⚠️ 'llama3' model not found. You may need to run 'ollama pull llama3'.")
        else:
            print(f"❌ Ollama returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Could not connect to Ollama: {e}")

if __name__ == "__main__":
    check_google_search()
    check_clearbit()
    check_lusha()
    check_email_verifier()
    check_ollama()
