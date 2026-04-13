import time
from datetime import datetime, timezone, timedelta
import json
import sys
import os

from playwright.sync_api import sync_playwright
from config import DB_PATH, BROWSER_PROFILE_DIR

from agents.job_search import JobSearchAgent
from agents.job_extraction import JobExtractionAgent
from agents.email_writer import EmailWriterAgent
from agents.email_sender import EmailSenderAgent
from agents.application_agent import ApplicationAgent
from agents.tracker_agent import tracker_agent

def is_within_working_hours():
    ist_offset = timedelta(hours=5, minutes=30)
    now_ist = datetime.now(timezone.utc) + ist_offset
    return 7 <= now_ist.hour < 22

def run_workflow():
    if not is_within_working_hours():
        print("Outside working hours (7 AM - 10 PM IST). Task queued.")
        return {"status": "queued"}

    print("Starting automated job application...")

    search_agent = JobSearchAgent()
    extract_agent = JobExtractionAgent()
    email_writer = EmailWriterAgent()
    email_sender = EmailSenderAgent()
    app_agent = ApplicationAgent()

    results = []

    try:
        os.makedirs(BROWSER_PROFILE_DIR, exist_ok=True)
        with sync_playwright() as p:
            print("Launching shared browser context...")
            browser = p.chromium.launch_persistent_context(
                user_data_dir=BROWSER_PROFILE_DIR, 
                headless=False,
                slow_mo=50
            )
            page = browser.new_page()

            tracker_agent.log(search_agent.name, "search_start", "success", {"keywords": "Data Scientist 0-2 years"})
            
            # 1. SEARCH
            search_result = search_agent.search_jobs(page, "Data Scientist 0-2 years", max_jobs=10) 
            
            if search_result['status'] == 'failed':
                tracker_agent.log(search_agent.name, "search_end", "failed", {}, search_result['error'])
                print(f"Search failed: {search_result['error']}")
                browser.close()
                return {"status": "failed", "error": search_result['error']}

            jobs = search_result['data'].get('jobs', [])
            tracker_agent.log(search_agent.name, "search_end", "success", {"jobs_found": len(jobs)})

            # 2. PROCESS JOBS
            for job in jobs:
                print(f"Processing job: {job['title']} at {job['company']}")
                
                # Deduplication logic
                if tracker_agent.is_already_contacted(job['company']):
                    print(f"Skipping [ALREADY CONTACTED]: {job['company']}")
                    tracker_agent.log(tracker_agent.name, "deduplication", "success", {"company": job['company'], "action": "skip"})
                    continue

                tracker_agent.log_job(job['id'], job['title'], job['company'], job['url'])
                
                # EXTRACT
                ext_result = extract_agent.extract_details(page, job['url'])
                if ext_result['status'] == 'failed':
                    tracker_agent.log(extract_agent.name, "extract", "failed", {"job_url": job['url']}, ext_result['error'])
                    continue
                    
                hr_email = ext_result['data'].get('hr_email')
                job_details = {**job, **ext_result['data']}
                
                if hr_email:
                    print(f"HR Email found: {hr_email}. Preparing email...")
                    writer_result = email_writer.write_email(job_details)
                    if writer_result['status'] == 'success':
                        subject = writer_result['data']['subject']
                        body = writer_result['data']['body']
                        print(f"Sending email to {hr_email}...")
                        
                        send_result = email_sender.send_email(hr_email, subject, body)
                        tracker_agent.log(email_sender.name, "send_email", send_result['status'], {"hr_email": hr_email}, send_result.get('error'))
                        
                        if send_result['status'] == 'success':
                            tracker_agent.log_email_sent(job['id'], hr_email, subject, body)
                        
                        results.append({"job": job['url'], "action": "email", "status": send_result['status']})
                    else:
                        tracker_agent.log(email_writer.name, "write_email", "failed", {"job_url": job['url']}, writer_result['error'])
                else:
                    print("No HR Email found. Applying via browser...")
                    apply_result = app_agent.apply_job(page, job['url'])
                    tracker_agent.log(app_agent.name, "apply_job", apply_result['status'], {"job_url": job['url']}, apply_result.get('error'))
                    
                    if apply_result['status'] == 'success':
                        tracker_agent.log_application(job['id'])
                        
                    results.append({"job": job['url'], "action": "apply", "status": apply_result['status']})

            print("Closing browser...")
            browser.close()

    except Exception as e:
        print(f"Workflow error: {str(e)}")
        tracker_agent.log("Workflow", "fatal_error", "failed", {}, str(e))
        return {"status": "failed", "error": str(e)}

    print("Workflow complete.")
    for res in results:
        print(res)
    
    return {"status": "success", "results": results}

if __name__ == "__main__":
    run_workflow()
