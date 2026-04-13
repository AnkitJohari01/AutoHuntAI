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

    def _format_response(self, status, data, error):
        return {
            "agent": self.name,
            "status": status,
            "data": data,
            "error": error
        }

tracker_agent = TrackerAgent()
