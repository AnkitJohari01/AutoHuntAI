import sys
import os
import re
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from playwright.sync_api import sync_playwright
from config import BROWSER_PROFILE_DIR

class JobExtractionAgent:
    def __init__(self):
        self.name = "JobExtractionAgent"
        self.email_pattern = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')

    def extract_details(self, page, job_url):
        try:
            page.goto(job_url, timeout=60000)
            
            try:
                page.wait_for_selector(".show-more-less-html__markup", timeout=10000)
                desc_element = page.query_selector(".show-more-less-html__markup")
                description = desc_element.inner_text() if desc_element else ""
            except:
                description = page.inner_text("body")

            emails = self.email_pattern.findall(description)
            hr_email = emails[0] if emails else None

            data = {
                "description": description[:1000],
                "hr_email": hr_email,
                "apply_link": job_url
            }

            return self._format_response("success", data, None)
        except Exception as e:
            return self._format_response("failed", None, str(e))

    def _format_response(self, status, data, error):
        return {
            "agent": self.name,
            "status": status,
            "data": data,
            "error": error
        }
