import sys
import os
import time
import uuid
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from playwright.sync_api import sync_playwright
from config import BROWSER_PROFILE_DIR
from agents.tracker_agent import tracker_agent

class JobSearchAgent:
    def __init__(self):
        self.name = "JobSearchAgent"

    def search_jobs(self, page, keywords, max_jobs=20):
        try:
            jobs = []
            
            # 1. NAUKRI SEARCH
            search_query_naukri = keywords.replace(" ", "-")
            url_naukri = f"https://www.naukri.com/{search_query_naukri}-jobs"
            page.goto(url_naukri, timeout=60000)
            try: page.wait_for_selector(".srp-jobtuple-wrapper", timeout=15000)
            except Exception: pass
            
            for _ in range(3):
                page.evaluate("window.scrollBy(0, 1000)")
                time.sleep(1)

            naukri_cards = page.query_selector_all(".srp-jobtuple-wrapper")
            for card in naukri_cards:
                if len(jobs) >= max_jobs / 2: break
                title_elem = card.query_selector(".title")
                company_elem = card.query_selector(".comp-name")
                job_url = None
                try: job_url = title_elem.get_attribute("href")
                except Exception: pass
                if title_elem and company_elem and job_url:
                    job = {"id": str(uuid.uuid4()), "title": title_elem.inner_text().strip(), "company": company_elem.inner_text().strip(), "url": job_url}
                    if not any(j['url'] == job['url'] for j in jobs): jobs.append(job)

            # 2. LINKEDIN SEARCH
            tracker_agent.log(self.name, "search_platform", "success", {"platform": "LinkedIn"})
            search_query_li = keywords.replace(" ", "%20")
            url_li = f"https://www.linkedin.com/jobs/search/?keywords={search_query_li}&location=India&f_E=1%2C2"
            page.goto(url_li, timeout=60000)
            try: 
                page.wait_for_selector(".job-card-container", timeout=20000) # Increased timeout
                time.sleep(3) # Wait for cards to populate
            except Exception: pass
            
            for _ in range(3):
                page.evaluate("window.scrollBy(0, 1000)")
                time.sleep(2) # Slower scroll for LinkedIn lazy loading
                
            li_cards = page.query_selector_all(".job-card-container")
            for card in li_cards:
                if len(jobs) >= max_jobs: break
                title_elem = card.query_selector(".job-card-list__title--link")
                company_elem = card.query_selector(".artdeco-entity-lockup__subtitle")
                job_url = None
                try: job_url = title_elem.get_attribute("href")
                except Exception: pass
                if title_elem and company_elem and job_url:
                    job_url = "https://www.linkedin.com" + job_url if job_url.startswith("/") else job_url
                    # Extract text and clean up
                    title_text = title_elem.inner_text().split("\n")[0].strip()
                    company_text = company_elem.inner_text().strip()
                    job = {"id": str(uuid.uuid4()), "title": title_text, "company": company_text, "url": job_url}
                    if not any(j['url'] == job['url'] for j in jobs): jobs.append(job)

            if len(jobs) == 0:
                return self._format_response("failed", None, "No jobs found. Bot protection might have blocked access.")

            return self._format_response("success", {"jobs": jobs}, None)
        except Exception as e:
            return self._format_response("failed", None, str(e))

    def _format_response(self, status, data, error):
        return {
            "agent": self.name,
            "status": status,
            "data": data,
            "error": error
        }
