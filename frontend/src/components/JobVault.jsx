import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { FiBriefcase } from 'react-icons/fi';

export default function JobVault() {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await axios.get(`http://${window.location.hostname}:8000/api/jobs`);
        setJobs(response.data);
      } catch (err) {}
    };

    fetchJobs();
    const interval = setInterval(fetchJobs, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ animation: 'fadeIn 0.5s ease' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '24px' }}>
        <FiBriefcase size={28} color="var(--brand-secondary)" />
        <h2 style={{ fontSize: '32px', fontWeight: 700 }}>Job Vault</h2>
      </div>

      <div className="glass-card" style={{ padding: '0', overflowX: 'auto' }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Role</th>
              <th>Company</th>
              <th>Discovery Time</th>
              <th>Apply URL</th>
            </tr>
          </thead>
          <tbody>
            {jobs.length === 0 ? (
              <tr>
                <td colSpan="5" style={{ textAlign: 'center', padding: '32px', color: 'var(--text-secondary)' }}>
                  Awaiting extraction pipeline data...
                </td>
              </tr>
            ) : (
              jobs.map((job, idx) => (
                <tr key={idx}>
                  <td style={{ fontFamily: 'Fira Code, monospace', fontSize: '13px' }}>{job.job_id}</td>
                  <td style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{job.title}</td>
                  <td>{job.company}</td>
                  <td style={{ color: 'var(--text-secondary)' }}>{job.discovered_at ? new Date(job.discovered_at + "Z").toLocaleString() : 'N/A'}</td>
                  <td>
                    <a href={job.url} target="_blank" rel="noopener noreferrer" style={{ color: 'var(--brand-primary)', textDecoration: 'none' }}>
                      {job.url ? `${job.url.substring(0, 30)}...` : 'Link'}
                    </a>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
