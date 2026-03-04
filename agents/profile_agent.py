import pdfplumber
import re
import spacy
from typing import Dict, Any
from utils.helpers import setup_logger, clean_text
from utils.regex_patterns import LINKEDIN_URL_PATTERN

logger = setup_logger("ProfileAgent")

class ProfileAgent:
    def __init__(self):
        try:
            # We wrap in try in case user needs to download explicitly
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.warning("Spacy model 'en_core_web_sm' not found. Falling back to simple regex extraction. To fix: python -m spacy download en_core_web_sm")
            self.nlp = None

    def extract_text(self, filepath: str) -> str:
        """Extract all text from a PDF."""
        text = ""
        try:
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            logger.error(f"Failed to read PDF {filepath}: {e}")
        return text.strip()

    def parse(self, filepath: str) -> Dict[str, Any]:
        """Extract structured data from PDF."""
        logger.info(f"Parsing profile: {filepath}")
        raw_text = self.extract_text(filepath)
        
        # We need heuristics, as LinkedIn PDF exports generally follow a specific format
        # Often starts with "First Last\nHeadline\nCompany" etc.
        lines = raw_text.split("\n")
        lines = [clean_text(l) for l in lines if l.strip()]
        
        profile = {
            "name": "Unknown",
            "company": "Unknown",
            "role": "Unknown",
            "linkedin": "Unknown"
        }
        
        if not lines:
            return profile

        first_line = lines[0]
        # Heuristic for Name and Role
        # The first non-empty line after cleaning.
        if lines[0].startswith("Contact"):
            # Name is often in the first line after "Contact"
            parts = lines[0].replace("Contact", "").strip().split()
            name_parts = []
            for p in parts:
                if "@" in p or len(name_parts) >= 4: # Stop at email or 4th word
                    break
                name_parts.append(p)
            profile["name"] = " ".join(name_parts)
            
            # Start looking for Role from next lines
            for line in lines[1:6]:
                cleaned_line = clean_text(line)
                # Skip lines that look like links, emails, or generic headers
                if "@" in cleaned_line or "linkedin.com" in cleaned_line or "Portfolio" in cleaned_line:
                    continue
                # If there's a leftover 'm ' or similar from a split email 'com'
                if cleaned_line.startswith('m ') and len(cleaned_line) > 2:
                    cleaned_line = cleaned_line[2:].strip()
                    
                if len(cleaned_line) < 5:
                    continue
                profile["role"] = cleaned_line[:100]
                break
        else:
            profile["name"] = lines[0][:50]
            if len(lines) > 1:
                profile["role"] = clean_text(lines[1][:100])
                
        # Finding explicitly mentioned linkedIn URL
        li_match = LINKEDIN_URL_PATTERN.search(raw_text)
        if li_match:
            profile["linkedin"] = li_match.group(0)

        # Naive company extraction: often looks for "Current: [Company]" or similar
        # Alternatively, we can use spaCy ORG recognition
        companies = []
        if self.nlp:
            doc = self.nlp(raw_text[:1000]) # look at top 1000 chars
            for ent in doc.ents:
                if ent.label_ == "ORG" and ent.text.lower() not in ["linkedin", "summary"]:
                    companies.append(ent.text)
                    
        if companies:
            # Filter out entries that look like the 'Contact' header or are just emails
            filtered_companies = []
            for c in companies:
                c_clean = clean_text(c)
                # If it's a role, it's not a company in this context
                if c_clean.lower() == profile["role"].lower():
                    continue
                if not c_clean or c_clean.lower() in ["linkedin", "summary", "contact"] or "@" in c_clean:
                    continue
                # If it's too long, it might be a sentence, not a company
                if len(c_clean.split()) > 6:
                    continue
                filtered_companies.append(c_clean)
            
            if filtered_companies:
                profile["company"] = filtered_companies[0]
        
        # If company still Unknown, see if we can find something in headline
        if profile["company"] == "Unknown" and " at " in profile["role"]:
            profile["company"] = profile["role"].split(" at ")[-1].strip()

        # Final cleanup for all fields
        for key in profile:
            profile[key] = clean_text(profile[key])

        logger.info(f"Extracted Profile: {profile}")
        return profile
