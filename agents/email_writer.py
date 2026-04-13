import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from llm_client import generate_text
from config import CANDIDATE

class EmailWriterAgent:
    def __init__(self):
        self.name = "EmailWriterAgent"

    def write_email(self, job_details):
        try:
            prompt = f"""
Write a personalized cold email (120-150 words) applying for the role of {job_details.get('title', 'a relevant role')} at {job_details.get('company', 'your company')}.

Use the following candidate information:
- Name: {CANDIDATE['name']}
- Experience: {CANDIDATE['experience']}
- Skills: {', '.join(CANDIDATE['skills'])}
- GitHub: {CANDIDATE['github']}
- LinkedIn: {CANDIDATE['linkedin']}

Instructions:
- Address the hiring manager or HR appropriately.
- Highlight how my skills align with the role.
- Include my Github and LinkedIn links exactly as provided.
- Include a clear call to action and mention the attached resume.
- Keep it concise and professional.
- Do NOT include any placeholders like [Your Name] because I will copy-paste this directly.
- Output ONLY the email body.
"""
            body = generate_text(prompt, system_prompt="You are a professional job seeking assistant. Output only the email text.")
            
            if not body:
                raise Exception("LLM returned empty response")

            subject = f"Application for {job_details.get('title', 'Role')} - {CANDIDATE['name']}"
            return self._format_response("success", {"subject": subject, "body": body}, None)
            
        except Exception as e:
            return self._format_response("failed", None, str(e))

    def _format_response(self, status, data, error):
        return {
            "agent": self.name,
            "status": status,
            "data": data,
            "error": error
        }
