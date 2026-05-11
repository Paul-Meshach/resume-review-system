# CONCEPT: Resume parsing is inherently messy — every resume has a different format
# Strategy: Use regex patterns to find structured data (email, phone, years of exp)
# For unstructured data (skills, name), use heuristics + keyword matching
# This will NOT be perfect — that's okay for an interview project
# Mention spaCy or OpenAI API as production-grade alternatives

import pdfplumber
import docx
import re
from typing import Optional
import os


# ──────────────────────────────────────────────
# EXTRACTION HELPERS
# ──────────────────────────────────────────────

def extract_email(text: str) -> Optional[str]:
    """Regex to find email — very reliable"""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(pattern, text)
    return match.group(0) if match else None


def extract_phone(text: str) -> Optional[str]:
    """Find Indian/international phone numbers"""
    pattern = r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)(\d{3}[-.\s]?\d{4})'
    match = re.search(pattern, text)
    return match.group(0).strip() if match else None


def extract_name(text: str) -> Optional[str]:
    """
    Heuristic: Name is usually in the first 3 lines
    Most resumes start with the candidate's name
    """
    lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
    for line in lines[:5]:
        # Skip lines with common non-name content
        if any(kw in line.lower() for kw in
               ['resume', 'curriculum', 'address', 'email', 'phone', 'mobile', '@', 'http']):
            continue
        # Name lines are typically 2-4 words, not too long
        words = line.split()
        if 1 < len(words) <= 5 and all(w.replace('.', '').isalpha() for w in words):
            return line
    return lines[0] if lines else None


def extract_experience(text: str) -> Optional[str]:
    """Find years of experience mentions"""
    patterns = [
        r'(\d+\.?\d*)\+?\s*years?\s+of\s+experience',
        r'experience[:\s]+(\d+\.?\d*)\+?\s*years?',
        r'(\d+\.?\d*)\+?\s*yrs?\s+exp',
        r'(\d+\.?\d*)\s*-\s*(\d+\.?\d*)\s*years?',
    ]
    text_lower = text.lower()
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            return match.group(0)
    return None


def extract_skills(text: str) -> str:
    """
    Match against a predefined skills dictionary
    Production alternative: Use NLP/NER model or skills taxonomy API
    """
    KNOWN_SKILLS = [
        # Languages
        'python', 'javascript', 'java', 'c++', 'c#', 'typescript', 'go', 'rust',
        'php', 'ruby', 'swift', 'kotlin', 'scala', 'r',
        # Frontend
        'react', 'angular', 'vue', 'html', 'css', 'tailwind', 'bootstrap',
        'next.js', 'gatsby', 'redux', 'jquery',
        # Backend
        'fastapi', 'django', 'flask', 'node.js', 'express', 'spring boot',
        'laravel', 'rails', '.net', 'asp.net',
        # Databases
        'sql server', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle',
        'sqlite', 'elasticsearch', 'cassandra',
        # Cloud/DevOps
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git',
        'github', 'gitlab', 'terraform', 'ansible', 'linux',
        # Data/ML
        'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'pandas',
        'numpy', 'scikit-learn', 'power bi', 'tableau', 'excel',
        # Other
        'rest api', 'graphql', 'microservices', 'agile', 'scrum', 'jira',
    ]

    text_lower = text.lower()
    found = [skill for skill in KNOWN_SKILLS if skill in text_lower]
    return ', '.join(found) if found else ''


def extract_qualification(text: str) -> Optional[str]:
    """Look for degree keywords"""
    degrees = [
        r'b\.?tech', r'm\.?tech', r'b\.?e\.?', r'm\.?e\.?',
        r'bachelor', r'master', r'mba', r'bca', r'mca',
        r'b\.?sc', r'm\.?sc', r'ph\.?d', r'diploma',
        r'b\.?com', r'm\.?com'
    ]
    text_lower = text.lower()
    for degree in degrees:
        match = re.search(degree, text_lower)
        if match:
            # Return surrounding context for more detail
            start = max(0, match.start() - 5)
            end = min(len(text), match.end() + 50)
            return text[start:end].strip().split('\n')[0]
    return None


def extract_domain(text: str) -> Optional[str]:
    """Identify the candidate's domain/industry"""
    domains = {
        'web development': ['web dev', 'frontend', 'backend', 'full stack', 'fullstack'],
        'data science': ['data science', 'machine learning', 'deep learning', 'data analyst'],
        'devops': ['devops', 'site reliability', 'cloud engineer', 'infrastructure'],
        'mobile development': ['android', 'ios', 'mobile app', 'flutter', 'react native'],
        'cybersecurity': ['security', 'penetration', 'ethical hacking', 'soc analyst'],
        'database administration': ['dba', 'database admin', 'sql server admin'],
        'ui/ux design': ['ui/ux', 'user experience', 'figma', 'wireframe'],
    }
    text_lower = text.lower()
    for domain, keywords in domains.items():
        if any(kw in text_lower for kw in keywords):
            return domain
    return 'software development'  # Default fallback


# ──────────────────────────────────────────────
# MAIN PARSER FUNCTIONS
# ──────────────────────────────────────────────

def extract_text_from_pdf(filepath: str) -> str:
    """Use pdfplumber to extract text from PDF files"""
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def extract_text_from_docx(filepath: str) -> str:
    """Use python-docx to extract text from DOCX files"""
    doc = docx.Document(filepath)
    paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
    return "\n".join(paragraphs)


def parse_resume(filepath: str) -> dict:
    """
    Main function — detects file type, extracts text, runs all extractors
    Returns a dict of all extracted fields
    """
    ext = os.path.splitext(filepath)[1].lower()

    if ext == '.pdf':
        text = extract_text_from_pdf(filepath)
    elif ext in ['.docx', '.doc']:
        text = extract_text_from_docx(filepath)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    if not text.strip():
        raise ValueError("Could not extract text from the resume file")

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "qualification": extract_qualification(text),
        "skills": extract_skills(text),
        "years_of_experience": extract_experience(text),
        "domain": extract_domain(text),
    }