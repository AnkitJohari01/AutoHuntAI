import os
import sys
import traceback
import logging
import anyio

# 1. FORCE WORKING DIRECTORY 
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_ROOT)
sys.path.append(PROJECT_ROOT)

# 2. FILE LOGGING SETUP
LOG_FILE = os.path.join(PROJECT_ROOT, "mcp_server.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filemode='a'
)
logger = logging.getLogger("mcp_server")
logger.info("MCP Server starting up (Sync-to-Async Bridge Mode)...")

# 3. CONFIGURE LOGGING TO STDERR AS WELL
console_handler = logging.StreamHandler(sys.stderr)
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

from typing import Optional
from playwright.sync_api import sync_playwright
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP
mcp = FastMCP("AutoHunt AI")

# Lazy Agent Initializer
def get_agents():
    logger.info("Initializing agents...")
    from agents.job_search import JobSearchAgent
    from agents.job_extraction import JobExtractionAgent
    from agents.application_agent import ApplicationAgent
    return JobSearchAgent(), JobExtractionAgent(), ApplicationAgent()

def cleanup_browser_locks():
    from config import BROWSER_PROFILE_DIR
    lock_file = os.path.join(BROWSER_PROFILE_DIR, "SingletonLock")
    if os.path.exists(lock_file):
        try:
            os.remove(lock_file)
            logger.info("Removed browser lock file.")
        except Exception as e:
            logger.warning(f"Could not remove lock file: {e}")

@mcp.tool()
async def echo_test(text: str) -> str:
    """A simple tool to verify the MCP connection is working."""
    logger.info(f"Echo tool called with: {text}")
    return f"AutoHunt MCP is active! You said: {text}"

# BRIDGE FUNCTION: Runs sync playwright logic safely in a separate thread
# This prevents the "Sync API used inside asyncio loop" error.
def _search_jobs_sync(keywords: str, max_jobs: int):
    from config import BROWSER_PROFILE_DIR
    search_agent, _, _ = get_agents()
    cleanup_browser_locks()
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=BROWSER_PROFILE_DIR, 
                headless=False,
                args=["--disable-blink-features=AutomationControlled"],
                slow_mo=50
            )
            page = browser.new_page()
            result = search_agent.search_jobs(page, keywords, max_jobs=max_jobs)
            browser.close()
            
            if result['status'] == 'success':
                jobs = result['data']['jobs']
                summary = f"Found {len(jobs)} jobs:\n"
                for i, job in enumerate(jobs, 1):
                    summary += f"{i}. {job['title']} at {job['company']} - {job['url']}\n"
                return summary
            return f"Search failed: {result['error']}"
    except Exception as e:
        logger.error(f"Search exception: {traceback.format_exc()}")
        return f"Error during search: {str(e)}"

@mcp.tool()
async def search_jobs(keywords: str, max_jobs: int = 5) -> str:
    """Search for jobs and return a list of titles and URLs."""
    logger.info(f"Async Search tool called: {keywords}")
    return await anyio.to_thread.run_sync(_search_jobs_sync, keywords, max_jobs)

def _apply_to_job_sync(job_url: str):
    from config import BROWSER_PROFILE_DIR
    _, _, app_agent = get_agents()
    cleanup_browser_locks()
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=BROWSER_PROFILE_DIR, 
                headless=False,
                slow_mo=100
            )
            page = browser.new_page()
            result = app_agent.apply_job(page, job_url)
            browser.close()
            if result['status'] == 'success':
                return f"Successfully applied to {job_url}"
            return f"Application failed: {result['error']}"
    except Exception as e:
        logger.error(f"Apply exception: {traceback.format_exc()}")
        return f"Error during application: {str(e)}"

@mcp.tool()
async def apply_to_job(job_url: str) -> str:
    """Automatically apply to a specific job URL."""
    logger.info(f"Async Apply tool called for: {job_url}")
    return await anyio.to_thread.run_sync(_apply_to_job_sync, job_url)

@mcp.tool()
async def get_stats() -> str:
    """Get statistics from the current job database."""
    import sqlite3
    from config import DB_PATH
    try:
        conn = sqlite3.connect(DB_PATH)
        total_jobs = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
        auto_apps = conn.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
        conn.close()
        return f"AutoHunt Stats:\n- Jobs in Vault: {total_jobs}\n- Automated Applications: {auto_apps}"
    except Exception as e:
        return f"Error fetching stats: {str(e)}"

if __name__ == "__main__":
    try:
        mcp.run()
    except Exception:
        logger.fatal(f"FATAL CRASH: {traceback.format_exc()}")
