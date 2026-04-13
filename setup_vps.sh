#!/ Maria/bin/bash

# ==============================================================================
# Autohunt-AI - VPS Setup Script for Ubuntu 22.04/24.04
# ==============================================================================

# 1. System Updates
echo "Updating system..."
sudo apt-get update && sudo apt-get upgrade -y

# 2. Install Dependencies
echo "Installing Python, Node.js, and essential tools..."
sudo apt-get install -y python3-pip python3-venv nodejs npm git curl

# 3. Install Ollama
echo "Installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

# 4. Pull the Lightweight Model
echo "Pulling Ollama model (qwen2.5:0.5b)..."
ollama pull qwen2.5:0.5b

# 5. Application Setup
echo "Configuring application environment..."
python3 -m venv ahenv
source ahenv/bin/activate
pip install -r requirements.txt || pip install playwright fastapi uvicorn ollama playwright-stealth
playwright install --with-deps chromium

# 6. Database Initialization
echo "Initializing database..."
python3 database.py

# 7. Frontend Build (Optional, if not using Dev server)
echo "Setting up frontend..."
cd frontend
npm install
# We will use 'npm run dev' for simplicity on the VPS for now
cd ..

echo "==============================================================================="
echo " SETUP COMPLETE! "
echo "==============================================================================="
echo "Next Steps:"
echo "1. Upload your 'data/browser_profile' folder to 'data/' on this server."
echo "2. Start Backend:  source ahenv/bin/activate && uvicorn api:app --host 0.0.0.0 --port 8000"
echo "3. Start Frontend: cd frontend && npm run dev -- --host 0.0.0.0"
echo "==============================================================================="
