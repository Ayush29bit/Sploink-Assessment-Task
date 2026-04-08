import { useState } from "react";
import SessionList from "./components/SessionList";
import SessionDetail from "./components/SessionDetail";
import "./App.css";

function App() {
  const [selectedSession, setSelectedSession] = useState(null);

  return (
    <div className="app">
      <header className="app-header">
        <h1> Agent Monitor</h1>
        <p className="subtitle">AI Agent Session Observability Dashboard</p>
      </header>
      <main className="app-main">
        {selectedSession ? (
          <SessionDetail
            sessionId={selectedSession}
            onBack={() => setSelectedSession(null)}
          />
        ) : (
          <SessionList onSelect={setSelectedSession} />
        )}
      </main>
    </div>
  );
}

export default App;
