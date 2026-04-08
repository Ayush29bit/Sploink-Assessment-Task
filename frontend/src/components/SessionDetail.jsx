import { useState, useEffect } from "react";
import { fetchSession } from "../api";

const STATUS_COLORS = {
  healthy: "#22c55e",
  failing: "#ef4444",
  drifting: "#f97316",
  looping: "#eab308",
  empty: "#6b7280",
};

const ACTION_ICONS = {
  read_file: "",
  write_file: "",
  run_command: "",
  llm_call: "",
};

export default function SessionDetail({ sessionId, onBack }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetchSession(sessionId)
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [sessionId]);

  if (loading) return <div className="loading">Loading session...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  const { events, metrics, status } = data;

  return (
    <div className="session-detail">
      <button className="back-btn" onClick={onBack}>
        ← Back to Sessions
      </button>

      <div className="detail-header">
        <h2>{sessionId}</h2>
        <span
          className="status-badge large"
          style={{ backgroundColor: STATUS_COLORS[status] }}
        >
          {status}
        </span>
      </div>

      {/* Metrics */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-value">{metrics.total_steps}</div>
          <div className="metric-label">Total Steps</div>
        </div>
        <div className="metric-card">
          <div className="metric-value success">
            {(metrics.success_rate * 100).toFixed(0)}%
          </div>
          <div className="metric-label">Success Rate</div>
        </div>
        <div className="metric-card">
          <div className="metric-value failure">
            {(metrics.failure_rate * 100).toFixed(0)}%
          </div>
          <div className="metric-label">Failure Rate</div>
        </div>
        <div className="metric-card">
          <div className="metric-value">
            {Object.keys(metrics.action_distribution).length}
          </div>
          <div className="metric-label">Unique Actions</div>
        </div>
      </div>

      {/* Action Distribution */}
      <div className="section">
        <h3>Action Distribution</h3>
        <div className="action-dist">
          {Object.entries(metrics.action_distribution).map(([action, count]) => (
            <div key={action} className="action-bar-row">
              <span className="action-name">
                {ACTION_ICONS[action] || "•"} {action}
              </span>
              <div className="action-bar-track">
                <div
                  className="action-bar-fill"
                  style={{
                    width: `${(count / metrics.total_steps) * 100}%`,
                  }}
                />
              </div>
              <span className="action-count">{count}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Events Timeline */}
      <div className="section">
        <h3>Events Timeline</h3>
        <div className="events-table-wrapper">
          <table className="events-table">
            <thead>
              <tr>
                <th>Step</th>
                <th>Action</th>
                <th>Input</th>
                <th>Output</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {events.map((e, i) => (
                <tr
                  key={i}
                  className={
                    e.metadata?.status === "failure" ? "row-failure" : ""
                  }
                >
                  <td>{e.step}</td>
                  <td>
                    {ACTION_ICONS[e.action] || ""} {e.action}
                  </td>
                  <td className="input-cell">{e.input || "—"}</td>
                  <td className="output-cell">{e.output || "—"}</td>
                  <td>
                    <span
                      className={`status-dot ${e.metadata?.status || "success"}`}
                    >
                      {e.metadata?.status || "success"}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
