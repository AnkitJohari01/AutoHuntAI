import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { FiMonitor } from 'react-icons/fi';

export default function Terminal() {
  const [logs, setLogs] = useState([]);
  const terminalEndRef = useRef(null);

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/logs');
        // Backend returns DESC limit 50, reverse to show chronological down
        setLogs(response.data.reverse());
      } catch (err) {}
    };

    fetchLogs();
    const interval = setInterval(fetchLogs, 2000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    terminalEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  return (
    <div style={{ animation: 'fadeIn 0.5s ease', height: '100%', display: 'flex', flexDirection: 'column' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '24px' }}>
        <FiMonitor size={28} color="var(--brand-primary)" />
        <h2 style={{ fontSize: '32px', fontWeight: 700 }}>Telemetry Stream</h2>
      </div>
      
      <div className="glass-card" style={{ flex: 1, padding: 0, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        <div style={{ background: 'rgba(0,0,0,0.4)', padding: '12px 24px', borderBottom: '1px solid var(--border-light)', display: 'flex', gap: '8px' }}>
          <div style={{width: 12, height: 12, borderRadius: '50%', background: '#ff5f56'}}></div>
          <div style={{width: 12, height: 12, borderRadius: '50%', background: '#ffbd2e'}}></div>
          <div style={{width: 12, height: 12, borderRadius: '50%', background: '#27c93f'}}></div>
        </div>
        
        <div className="terminal-window" style={{ flex: 1, border: 'none', borderRadius: '0 0 var(--radius-lg) var(--radius-lg)' }}>
          {logs.length === 0 ? (
            <div style={{ color: 'var(--text-secondary)' }}>Awaiting telemetry signals...</div>
          ) : (
            logs.map((log, idx) => (
              <div key={idx} className="terminal-line" style={{ animationDelay: `${Math.min(idx * 0.05, 1)}s` }}>
                <span className="log-time">[{new Date(log.timestamp).toLocaleTimeString()}]</span>
                <span className="log-agent">{log.agent}</span>
                <span style={{ color: '#d8dee9', width: '120px' }}>&gt; {log.action}</span>
                <span className={log.status === 'success' ? 'log-success' : log.status === 'failed' ? 'log-failed' : ''} style={{ textTransform: 'uppercase', fontSize: '11px', fontWeight: 'bold' }}>
                  [{log.status}]
                </span>
                {log.error && <span style={{ color: '#bf616a' }}> - ERRR: {log.error}</span>}
              </div>
            ))
          )}
          <div ref={terminalEndRef} />
        </div>
      </div>
    </div>
  );
}
