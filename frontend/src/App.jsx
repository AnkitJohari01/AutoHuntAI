import React, { useState } from 'react';
import { FiHome, FiTerminal, FiBriefcase, FiPlay, FiLoader, FiMail } from 'react-icons/fi';
import Dashboard from './components/Dashboard';
import Terminal from './components/Terminal';
import JobVault from './components/JobVault';
import EmailLog from './components/EmailLog';
import axios from 'axios';
import './index.css';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isAutomationRunning, setIsAutomationRunning] = useState(false);

  const startAutomation = async () => {
    try {
      setIsAutomationRunning(true);
      await axios.post('http://127.0.0.1:8000/api/run');
      // Set a timeout to reset the button eventually
      setTimeout(() => setIsAutomationRunning(false), 20000); 
    } catch (e) {
      console.error(e);
      alert('Failed to start automation. Is FastAPI backend running?');
      setIsAutomationRunning(false);
    }
  };

  const navItemStyle = (tabId) => ({
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    padding: '12px',
    borderRadius: '8px',
    background: activeTab === tabId ? 'rgba(255,255,255,0.1)' : 'transparent',
    color: activeTab === tabId ? 'var(--text-primary)' : 'var(--text-secondary)',
    transition: 'all 0.2s',
    fontWeight: activeTab === tabId ? 600 : 400
  });

  return (
    <div className="app-container">
      <aside className="sidebar">
        <h1 style={{ marginBottom: '40px', fontSize: '24px', background: 'var(--brand-gradient)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
          AutoHunt AI
        </h1>
        
        <nav style={{ display: 'flex', flexDirection: 'column', gap: '8px', flex: 1 }}>
          <div style={navItemStyle('dashboard')} onClick={() => setActiveTab('dashboard')}>
            <FiHome size={20} /> <span>Dashboard</span>
          </div>
          <div style={navItemStyle('terminal')} onClick={() => setActiveTab('terminal')}>
            <FiTerminal size={20} /> <span>Live Terminal</span>
          </div>
          <div style={navItemStyle('vault')} onClick={() => setActiveTab('vault')}>
            <FiBriefcase size={20} /> <span>Job Vault</span>
          </div>
          <div style={navItemStyle('emails')} onClick={() => setActiveTab('emails')}>
            <FiMail size={20} /> <span>Email Log</span>
          </div>
        </nav>

        <div style={{ marginTop: 'auto', borderTop: '1px solid var(--border-light)', paddingTop: '20px' }}>
          <button 
            className="btn-primary" 
            style={{ 
              width: '100%', 
              background: isAutomationRunning ? 'rgba(255,255,255,0.1)' : 'var(--brand-gradient)',
              cursor: isAutomationRunning ? 'not-allowed' : 'pointer'
            }}
            onClick={startAutomation}
            disabled={isAutomationRunning}
          >
            {isAutomationRunning ? <FiLoader /> : <FiPlay />}
            {isAutomationRunning ? 'Engine Active...' : 'Launch Protocol'}
          </button>
        </div>
      </aside>

      <main className="main-content">
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'terminal' && <Terminal />}
        {activeTab === 'vault' && <JobVault />}
        {activeTab === 'emails' && <EmailLog />}
      </main>
    </div>
  );
}

export default App;
