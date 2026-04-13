import sys
import os
import time

from playwright.sync_api import sync_playwright
from config import BROWSER_PROFILE_DIR

def open_browser_for_login():
    print("Opening Playwright browser...")
    print("Please log in to LinkedIn and Naukri in the opened browser window.")
    print("Once you are logged in, close the browser window to save your session.")
    
    os.makedirs(BROWSER_PROFILE_DIR, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=BROWSER_PROFILE_DIR, 
            headless=False,
            # viewport={"width": 1280, "height": 720}
        )
        
        page1 = browser.new_page()
        page1.goto("https://www.linkedin.com/login", timeout=60000)
        
        page2 = browser.new_page()
        page2.goto("https://www.naukri.com/nlogin/login", timeout=60000)
        
        print("\nWaiting for you to close the browser...")
        
        # Keep the script running until the browser context is closed by the user
        try:
            while len(browser.pages) > 0:
                time.sleep(1)
        except Exception:
            pass
            
        print("Browser closed. Session cookies saved successfully!")

if __name__ == "__main__":
    open_browser_for_login()
