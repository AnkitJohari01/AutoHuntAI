import { useState, useEffect } from "react";
import axios from "axios";
import { MdEmail, MdCheckCircle, MdError, MdRefresh } from "react-icons/md";

export default function EmailLog() {
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchEmails = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`http://${window.location.hostname}:8000/api/emails`);
      setEmails(res.data);
    } catch (e) {
      setEmails([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEmails();
    const interval = setInterval(fetchEmails, 15000);
    return () => clearInterval(interval);
  }, []);

  const successCount = emails.filter(e => e.status === "success").length;
  const failCount = emails.filter(e => e.status !== "success").length;

  return (
    <div className="page-content">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "2rem" }}>
        <h1 style={{ display: "flex", alignItems: "center", gap: "0.75rem", fontSize: "2rem", fontWeight: 700 }}>
          <MdEmail size={32} color="var(--accent)" />
          Email Intelligence
        </h1>
        <button className="btn-primary" onClick={fetchEmails} style={{ display: "flex", alignItems: "center", gap: "0.5rem", padding: "0.5rem 1.2rem" }}>
          <MdRefresh /> Refresh
        </button>
      </div>

      {/* Stats Row */}
      <div style={{ display: "flex", gap: "1.5rem", marginBottom: "2rem" }}>
        <div className="card" style={{ flex: 1 }}>
          <div style={{ color: "var(--text-muted)", fontSize: "0.8rem", textTransform: "uppercase", letterSpacing: "0.1em" }}>Total Sent</div>
          <div style={{ fontSize: "2.5rem", fontWeight: 800, color: "var(--accent)", marginTop: "0.5rem" }}>{emails.length}</div>
        </div>
        <div className="card" style={{ flex: 1 }}>
          <div style={{ color: "var(--text-muted)", fontSize: "0.8rem", textTransform: "uppercase", letterSpacing: "0.1em" }}>Delivered</div>
          <div style={{ fontSize: "2.5rem", fontWeight: 800, color: "#22c55e", marginTop: "0.5rem" }}>{successCount}</div>
        </div>
        <div className="card" style={{ flex: 1 }}>
          <div style={{ color: "var(--text-muted)", fontSize: "0.8rem", textTransform: "uppercase", letterSpacing: "0.1em" }}>Failed</div>
          <div style={{ fontSize: "2.5rem", fontWeight: 800, color: "#ef4444", marginTop: "0.5rem" }}>{failCount}</div>
        </div>
      </div>

      {/* Email Table */}
      <div className="card" style={{ padding: 0, overflow: "hidden" }}>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ borderBottom: "1px solid rgba(255,255,255,0.08)", background: "rgba(255,255,255,0.03)" }}>
              <th style={thStyle}>STATUS</th>
              <th style={thStyle}>RECIPIENT (HR EMAIL)</th>
              <th style={thStyle}>TIMESTAMP</th>
              <th style={thStyle}>NOTES</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={4} style={{ textAlign: "center", padding: "3rem", color: "var(--text-muted)" }}>Loading email history...</td></tr>
            ) : emails.length === 0 ? (
              <tr><td colSpan={4} style={{ textAlign: "center", padding: "3rem", color: "var(--text-muted)" }}>No emails dispatched yet. Click Launch Protocol to begin.</td></tr>
            ) : (
              emails.map((email, i) => (
                <tr key={i} style={{ borderBottom: "1px solid rgba(255,255,255,0.05)", transition: "background 0.2s" }}
                  onMouseEnter={e => e.currentTarget.style.background = "rgba(255,255,255,0.04)"}
                  onMouseLeave={e => e.currentTarget.style.background = "transparent"}>
                  <td style={tdStyle}>
                    <span style={{ display: "flex", alignItems: "center", gap: "0.4rem", color: email.status === "success" ? "#22c55e" : "#ef4444", fontWeight: 700, fontSize: "0.8rem" }}>
                      {email.status === "success" ? <MdCheckCircle size={16}/> : <MdError size={16}/>}
                      {email.status.toUpperCase()}
                    </span>
                  </td>
                  <td style={{ ...tdStyle, fontWeight: 600, color: email.status === "success" ? "var(--accent)" : "var(--text-muted)" }}>
                    {email.recipient}
                  </td>
                  <td style={{ ...tdStyle, color: "var(--text-muted)", fontSize: "0.85rem" }}>
                    {new Date(email.timestamp).toLocaleString("en-IN")}
                  </td>
                  <td style={{ ...tdStyle, color: "var(--text-muted)", fontSize: "0.8rem", maxWidth: "300px", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                    {email.status === "success" ? "✓ Delivered with resume attached" : (email.error || "Unknown error")}
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

const thStyle = {
  padding: "1rem 1.5rem",
  textAlign: "left",
  fontSize: "0.75rem",
  fontWeight: 700,
  color: "var(--text-muted)",
  letterSpacing: "0.1em",
  textTransform: "uppercase"
};

const tdStyle = {
  padding: "1rem 1.5rem",
};
