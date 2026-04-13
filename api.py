from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os

from main import run_workflow
from config import DB_PATH

app = FastAPI(title="Autohunt API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=404, detail="Database not initialized yet.")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/api/status")
def get_status():
    return {"status": "online"}

@app.post("/api/run")
def start_automation(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_workflow)
    return {"message": "Automation workflow successfully dispatched"}

@app.get("/api/logs")
def fetch_logs():
    try:
        conn = get_db_connection()
        logs = conn.execute("SELECT * FROM logs ORDER BY id DESC LIMIT 50").fetchall()
        conn.close()
        return [dict(l) for l in logs]
    except Exception as e:
        print(f"Error fetching logs: {e}")
        return []

@app.get("/api/jobs")
def fetch_jobs():
    try:
        conn = get_db_connection()
        jobs = conn.execute("SELECT * FROM jobs ORDER BY discovered_at DESC LIMIT 50").fetchall()
        conn.close()
        return [dict(j) for j in jobs]
    except Exception as e:
        print(f"Error fetching jobs: {e}")
        return []

@app.get("/api/emails")
def fetch_emails():
    """Returns full email send history - recipient, status, timestamp."""
    try:
        conn = get_db_connection()
        import json
        rows = conn.execute(
            "SELECT agent, action, status, details, error, timestamp FROM logs WHERE action='send_email' ORDER BY id DESC LIMIT 50"
        ).fetchall()
        conn.close()
        results = []
        for r in rows:
            detail = json.loads(r["details"]) if r["details"] else {}
            results.append({
                "timestamp": r["timestamp"],
                "status": r["status"],
                "recipient": detail.get("hr_email", "N/A"),
                "error": r["error"]
            })
        return results
    except Exception as e:
        print(f"Error fetching emails: {e}")
        return []

@app.get("/api/stats")
def fetch_stats():
    """Returns aggregate dashboard stats."""
    try:
        conn = get_db_connection()
        total_jobs = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
        # Count unique successful emails from the dedicated emails table
        emails_sent = conn.execute("SELECT COUNT(*) FROM emails WHERE sent_status='success'").fetchone()[0]
        # Count unique successful browser apps from the dedicated applications table
        auto_apps = conn.execute("SELECT COUNT(*) FROM applications WHERE status='success'").fetchone()[0]
        conn.close()
        return {"total_jobs": total_jobs, "emails_sent": emails_sent, "auto_apps": auto_apps}
    except Exception as e:
        print(f"Error fetching stats: {e}")
        return {"total_jobs": 0, "emails_sent": 0, "auto_apps": 0}
