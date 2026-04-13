import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from playwright.sync_api import sync_playwright
from config import BROWSER_PROFILE_DIR

class ApplicationAgent:
    def __init__(self):
        self.name = "ApplicationAgent"

    def apply_job(self, page, job_url):
        try:
            page.goto(job_url, timeout=60000)
            
            apply_buttons = page.locator("button:has-text('Apply'), button:has-text('Easy Apply')").all()
            if apply_buttons:
                for btn in apply_buttons:
                    if btn.is_visible():
                        btn.click()
                        time.sleep(3)
                        break
                
                for _ in range(5):
                    time.sleep(2)
                    next_btns = page.locator("button:has-text('Next'), button:has-text('Review')").all()
                    if next_btns:
                        for nb in next_btns:
                            if nb.is_visible():
                                nb.click()
                                break
                    else:
                        submit_btns = page.locator("button:has-text('Submit application')").all()
                        if submit_btns:
                            for sb in submit_btns:
                                if sb.is_visible():
                                    sb.click()
                                    break
                            break

            return self._format_response("success", {"application_status": "applied", "job_url": job_url}, None)
        except Exception as e:
            return self._format_response("failed", None, str(e))

    def _format_response(self, status, data, error):
        return {
            "agent": self.name,
            "status": status,
            "data": data,
            "error": error
        }
