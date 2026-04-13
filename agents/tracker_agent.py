import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database import get_connection
import json

class TrackerAgent:
    def __init__(self):
        self.name = "TrackerAgent"

    def log(self, agent_name, action, status_result, details_dict, error=None):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO logs (agent, action, status, details, error) VALUES (?, ?, ?, ?, ?)",
                (agent_name, action, status_result, json.dumps(details_dict), error)
            )
            conn.commit()
            conn.close()
            return self._format_response("success", {"logged": True}, None)
        except Exception as e:
            return self._format_response("failed", None, str(e))

    def log_job(self, job_id, title, company, url):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO jobs (job_id, title, company, url) 
                VALUES (?, ?, ?, ?)
            ''', (job_id, title, company, url))
            conn.commit()
            conn.close()
            return self._format_response("success", {"logged": True}, None)
        except Exception as e:
            return self._format_response("failed", None, str(e))

    def is_already_contacted(self, company):
        """Checks if we have already emailed or applied to this company."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Use LIKE for case-insensitive and partial matching if needed, 
            # but start with exact match for safety
            
            # Check emails table
            cursor.execute("SELECT COUNT(*) FROM emails WHERE job_id IN (SELECT job_id FROM jobs WHERE company = ?)", (company,))
            email_count = cursor.fetchone()[0]
            
            # Check applications table
            cursor.execute("SELECT COUNT(*) FROM applications WHERE job_id IN (SELECT job_id FROM jobs WHERE company = ?)", (company,))
            app_count = cursor.fetchone()[0]
            
            conn.close()
            return email_count > 0 or app_count > 0
        except Exception:
            return False

    def log_application(self, job_id):
        """Records a successful browser application."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO applications (job_id, status) VALUES (?, ?)", (job_id, "success"))
            conn.commit()
            conn.close()
        except Exception:
            pass

    def log_email_sent(self, job_id, email, subject, body):
        """Records a successful cold email."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO emails (job_id, recipient_email, subject, body, sent_status) VALUES (?, ?, ?, ?, ?)",
                (job_id, email, subject, body, "success")
            )
            conn.commit()
            conn.close()
        except Exception:
            pass

    def _format_response(self, status, data, error):
        return {
            "agent": self.name,
            "status": status,
            "data": data,
            "error": error
        }

tracker_agent = TrackerAgent()
