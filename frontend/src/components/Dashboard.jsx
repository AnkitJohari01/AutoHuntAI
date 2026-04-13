import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { FiTrendingUp, FiMail, FiCheckCircle } from 'react-icons/fi';

export default function Dashboard() {
  const [stats, setStats] = useState({ total_jobs: 0, emails_sent: 0, auto_apps: 0 });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await axios.get(`http://${window.location.hostname}:8000/api/stats`);
        setStats(res.data);
      } catch (err) {
        console.error("FastAPI Backend Offline");
      }
    };

    fetchStats();
    const interval = setInterval(fetchStats, 5000);
    return () => clearInterval(interval);
  }, []);


  return (
    <div style={{ animation: 'fadeIn 0.5s ease' }}>
      <h2 style={{ marginBottom: '32px', fontSize: '32px', fontWeight: 700 }}>Executive Overview</h2>
      
      <div className="metrics-grid">
        <div className="glass-card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', color: 'var(--text-secondary)' }}>
            <FiTrendingUp size={24} color="var(--brand-primary)" />
            <h3 style={{ fontSize: '13px', textTransform: 'uppercase', letterSpacing: '1px' }}>Total Jobs Found</h3>
          </div>
          <div className="metric-stat">{stats.total_jobs}</div>
        </div>

        <div className="glass-card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', color: 'var(--text-secondary)' }}>
            <FiMail size={24} color="var(--status-warning)" />
            <h3 style={{ fontSize: '13px', textTransform: 'uppercase', letterSpacing: '1px' }}>Emails Sent</h3>
          </div>
          <div className="metric-stat">{stats.emails_sent}</div>
        </div>

        <div className="glass-card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', color: 'var(--text-secondary)' }}>
            <FiCheckCircle size={24} color="var(--status-success)" />
            <h3 style={{ fontSize: '13px', textTransform: 'uppercase', letterSpacing: '1px' }}>Auto Apps</h3>
          </div>
          <div className="metric-stat">{stats.auto_apps}</div>
        </div>
      </div>
      
      <div className="glass-card" style={{ marginTop: '32px' }}>
        <h3 style={{ marginBottom: '16px' }}>System Architecture</h3>
        <p style={{ color: 'var(--text-secondary)', lineHeight: 1.6 }}>
          100% Free & Local Automations. <br/>
          Ollama LLMs + Playwright Engines + SQLite Storage.<br/>
          API Gateway listening at <code style={{ color: 'var(--text-accent)' }}>127.0.0.1:8000</code>.
        </p>
      </div>
    </div>
  );
}
