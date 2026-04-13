import os

# Candidate Information
CANDIDATE = {
    "name": "Your Full Name",
    "experience": "X years",
    "skills": [
        "Python", "Machine Learning", "Deep Learning",
        "Natural Language Processing (NLP)", "Generative AI",
        "Large Language Models (LLMs)", "LangChain", "SQL",
        "Docker", "AWS", "Streamlit", "React"
    ],
    "github": "https://github.com/YourUsername",
    "linkedin": "https://www.linkedin.com/in/your-profile/",
    "resume": r"C:\Path\To\Your\Resume.pdf"
}

# Email Configuration
# Use a Google App Password — NOT your normal Gmail password
# Generate one at: https://myaccount.google.com/apppasswords
EMAIL_USER = "your-email@gmail.com"
EMAIL_PASS = "your-16-char-google-app-password"

# LLM Model (must be pulled via: ollama pull <model>)
OLLAMA_MODEL = "qwen2.5:0.5b"   # Lightweight. Also works: gemma2:2b, phi3

# Paths
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "jobs.db")
BROWSER_PROFILE_DIR = os.path.join(os.path.dirname(__file__), "data", "browser_profile")
