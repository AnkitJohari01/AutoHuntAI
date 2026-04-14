# 🤖 AutoHunt AI — Automated Job Application Platform

A fully automated, **100% free and local** job application platform powered by Playwright, Ollama LLMs, FastAPI, and React.

## ✨ Features

- 🔍 **Dual-platform job search** — LinkedIn + Naukri simultaneously
- 🧠 **AI cold email generation** — Powered by local Ollama LLMs (no paid API)
- 📎 **Auto resume attachment** — Sends your PDF resume with every cold email
- 🖥️ **Real-time dashboard** — React UI with live telemetry stream & job vault
- 📧 **Email Intelligence tab** — Track every email dispatch with recipient & status
- 🍪 **Persistent sessions** — Uses your authenticated browser profile to avoid bot detection

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Browser Automation | Playwright (Chromium) |
| LLM Engine | Ollama (`qwen2.5:0.5b`) |
| Backend API | FastAPI + Uvicorn |
| Database | SQLite |
| Frontend | React + Vite |
| Email | SMTP via Gmail (App Password) |

---

## ⚡ Setup

### 1. Clone & Create Virtual Environment
```bash
git clone https://github.com/AnkitJohari01/AutoHuntAI.git
cd AutoHuntAI
python -m venv ahenv
ahenv\Scripts\activate
pip install playwright fastapi uvicorn ollama
playwright install chromium
```

### 2. Configure
```bash
cp config.example.py config.py
# Edit config.py with your details
```

### 3. Pull Ollama Model
```bash
ollama pull qwen2.5:0.5b
```

### 4. Login to LinkedIn & Naukri (One-time)
```bash
python login_browser.py
# Manually log into both platforms, then close the browser
```

### 5. Initialize Database
```bash
python database.py
```

### 6. Install Frontend Dependencies
```bash
cd frontend
npm install
cd ..
```

---

## 🚀 Run the App

**Terminal 1 — Backend:**
```bash
.\ahenv\Scripts\uvicorn api:app --host 127.0.0.1 --port 8000
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```

Open **[http://localhost:5173](http://localhost:5173)** and click **"Launch Protocol"** 🚀

---

## 📋 How It Works

```
Launch Protocol
     ↓
JobSearchAgent  →  Searches LinkedIn + Naukri
     ↓
JobExtractionAgent  →  Extracts HR email from job description
     ↓
  HR Email found?
  ├── YES → EmailWriterAgent (Ollama LLM) → EmailSenderAgent (Gmail SMTP)
  └── NO  → ApplicationAgent (Playwright auto-apply)
     ↓
TrackerAgent  →  Logs everything to SQLite → Dashboard updates
```

---

## ⚠️ Important Notes

- **Never commit `config.py`** — it contains your Gmail App Password
- Requires **2-Step Verification** on Gmail to generate an App Password
- Ollama must be running in the background for email generation
- Login sessions are stored in `data/browser_profile/` (also gitignored)

---

## 📸 Dashboard Preview

| Dashboard | Live Terminal | Job Vault | Email Log |
|---|---|---|---|
---

## 🤖 MCP Integration (Conversational Automation)

You can now control AutoHunt AI directly through **Claude Desktop** or other MCP clients.

### 1. Requirements
Ensure you have the MCP server dependencies installed:
```bash
.\ahenv\Scripts\pip install mcp mcp-cli
```

### 2. Configure Claude Desktop
Add the following to your `claude_desktop_config.json` (usually in `%APPDATA%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "autohunt": {
      "command": "python",
      "args": ["D:/Ankit/Autohunt-AI/mcp_server.py"],
      "env": {
        "PYTHONPATH": "D:/Ankit/Autohunt-AI"
      }
    }
  }
}
```
*Note: Ensure the paths above match your actual project location.*

### 3. Usage
Once configured, restart Claude Desktop. You can now use commands like:
- "Search for Data Science jobs in Bangalore"
- "Apply to this job: [link]"
- "Show me my application stats"

---

*Built with ❤️ by [Ankit Johari](https://www.linkedin.com/in/ankitjohari-s0217/)*
