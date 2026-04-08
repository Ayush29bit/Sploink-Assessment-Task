import { useState, useEffect } from "react";
import { fetchSessions, fetchSession } from "../api";

const STATUS_COLORS = {
  healthy: "#22c55e",
  failing: "#ef4444",
  drifting: "#f97316",
  looping: "#eab308",
  empty: "#6b7280",
};

export default function SessionList({ onSelect }) {
  const [sessions, setSessions] = useState([]);
  const [sessionData, setSessionData] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadSessions = async () => {
    setLoading(true);
    setError(null);
    try {
      const list = await fetchSessions();
      setSessions(list);
      // Fetch status for each session
      const dataMap = {};
      await Promise.all(
        list.map(async (id) => {
          try {
            const data = await fetchSession(id);
            dataMap[id] = data;
          } catch {
            dataMap[id] = null;
          }
        })
      );
      setSessionData(dataMap);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSessions();
  }, []);

  if (loading) return <div className="loading">Loading sessions...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="session-list">
      <div className="list-header">
        <h2>Agent Sessions</h2>
        <button className="refresh-btn" onClick={loadSessions}>
          ↻ Refresh
        </button>
      </div>
      {sessions.length === 0 ? (
        <div className="empty-state">
          <p>No sessions found.</p>
          <p className="hint">
            Run the simulator to generate sessions:
            <code>python simulator/agent.py --scenario normal</code>
          </p>
        </div>
      ) : (
        <div className="cards">
          {sessions.map((id) => {
            const data = sessionData[id];
            const status = data?.status || "empty";
            const metrics = data?.metrics;
            return (
              <div key={id} className="card" onClick={() => onSelect(id)}>
                <div className="card-header">
                  <span className="session-id">{id}</span>
                  <span
                    className="status-badge"
                    style={{ backgroundColor: STATUS_COLORS[status] }}
                  >
                    {status}
                  </span>
                </div>
                {metrics && (
                  <div className="card-metrics">
                    <span>{metrics.total_steps} steps</span>
                    <span>
                      {(metrics.success_rate * 100).toFixed(0)}% success
                    </span>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
