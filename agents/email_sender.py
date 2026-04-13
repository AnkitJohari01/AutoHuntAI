import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import smtplib
from email.message import EmailMessage
from config import EMAIL_USER, EMAIL_PASS, CANDIDATE

class EmailSenderAgent:
    def __init__(self):
        self.name = "EmailSenderAgent"

    def send_email(self, recipient_email, subject, body):
        try:
            if not EMAIL_USER or not EMAIL_PASS:
                raise ValueError("Email credentials missing in config.")

            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = EMAIL_USER
            msg['To'] = recipient_email
            msg.set_content(body)

            # Robust resume path finding
            possible_paths = [
                CANDIDATE['resume'],                                                # User's configured path
                os.path.join(os.path.dirname(os.path.dirname(__file__)), "Ankit_S_Johari.pdf"), # Project root (Windows)
                os.path.join(os.getcwd(), "Ankit_S_Johari.pdf"),                     # Current working directory
                r"D:\Ankit\Ankit_S_Johari.pdf"                                       # Hardcoded fallback
            ]
            
            resume_path = None
            for p in possible_paths:
                if p and os.path.exists(p):
                    resume_path = p
                    break

            if resume_path:
                with open(resume_path, 'rb') as f:
                    pdf_data = f.read()
                file_name = os.path.basename(resume_path)
                msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename=file_name)
            else:
                raise ValueError(f"Resume file not found. Searched: {possible_paths}")

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_USER, EMAIL_PASS)
                smtp.send_message(msg)

            return self._format_response("success", {"sent_to": recipient_email}, None)
        except Exception as e:
            return self._format_response("failed", None, str(e))

    def _format_response(self, status, data, error):
        return {
            "agent": self.name,
            "status": status,
            "data": data,
            "error": error
        }
