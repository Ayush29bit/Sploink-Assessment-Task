# Sploink Assessment Task

## Features

- ✅ Real-time event ingestion
- ✅ Session-based event tracking
- ✅ Metrics calculation and analysis
- ✅ Anomaly detection
- ✅ Interactive dashboard
- ✅ RESTful API
- ✅ CORS-enabled for cross-origin requests
- ✅ Responsive UI design

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React + Vite)                 │
│                    Port: 5173 (development)                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  SessionList    │    SessionDetail    │   Metrics   │    │
│  └─────────────────────────────────────────────────────┘    │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTP (JSON)
                             ▼
┌─────────────────────────────────────────────────────────────┐
│              Backend API (FastAPI)                          │
│                 Port: 8000                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  POST /events      │  GET /sessions                  │   │
│  │  GET /sessions/:id │  Metrics & Detection            │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│              Event Database & Analysis                      │
│  - Session Storage      - Event Processing                  │
│  - Metrics Calculation  - Anomaly Detection                 │
└─────────────────────────────────────────────────────────────┘
         ▲
         │ Event Simulation
         │
┌─────────────────────────────────────────────────────────────┐
│     Event Simulator (Python Agent)                          │
│  - Generates test sessions     - Simulates various scenarios│
└─────────────────────────────────────────────────────────────┘
```




## Installation & Setup

### 1. Clone and Setup Project Directory

```bash
cd Sploink-Assessment-Task
```

### 2. Backend Setup

#### Create and activate Python virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Install backend dependencies:

```bash
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend
npm install
cd ..
```

## Running the Application

### Option A: Run Everything (Recommended for Development)

You can start all services in separate terminals:

**Terminal 1 - Backend API:**
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Terminal 3 - Event Simulator (optional):**
```bash
python simulator/agent.py --scenario normal
```

### Option B: Individual Component Startup

#### Start Backend API
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

#### Start Frontend Development Server
```bash
cd frontend
npm run dev
```

The dashboard will be available at `http://localhost:5173`

#### Run Event Simulator
```bash
python simulator/agent.py --scenario {scenario_name}
```

Available scenarios:
- `normal` - Standard user session behavior
- `drift` - Gradual pattern changes
- `anomaly` - Unusual activity detection
- `custom` - Custom event generation

## API Endpoints

### Sessions

**Get All Sessions**
```
GET /sessions
Response: { "sessions": [...] }
```

**Get Session Details**
```
GET /sessions/{session_id}
Response: { "events": [...], "metrics": {...}, "status": {...} }
```

### Events

**Ingest New Event**
```
POST /events
Body: {
  "session_id": "string",
  "timestamp": number,
  "step": number,
  "action": "read_file|write_file|run_command|llm_call",
  "input": "string",
  "output": "string",
  "metadata": {
    "file": "string",
    "status": "success|failure"
  }
}
Response: { "status": "event received" }
```

## Environment Configuration

### Frontend Environment Variables

Create a `.env` file in the `frontend/` directory:

```env
VITE_API_URL=http://localhost:8000
```

### Backend Configuration

The backend uses environment variables for configuration. Create a `.env` file in the `backend/` directory if needed:

```env
DATABASE_URL=sqlite:///./sessions.db
LOG_LEVEL=INFO
```

## Development Workflow

1. **Start the backend API** (Terminal 1)
2. **Start the frontend dev server** (Terminal 2)
3. **Run the simulator** to generate test data (Terminal 3, optional)
4. **Access the dashboard** at `http://localhost:5173`

### Frontend Development

The frontend uses:
- **Vite** - Fast build tool and dev server
- **React 19** - UI framework

### Backend Development

The backend uses:
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **CORS Middleware** - Cross-origin request handling

## Detection Logic

The system uses heuristic-based behavioral analysis instead of naive rules.

### Loop Detection

Detects repeated behavior patterns using:

Consecutive identical actions
Dominant action ratio

Heuristics:

≥ 3 consecutive identical actions → loop
Dominant action > 80% of total steps → loop

### Drift Detection

Detects changes in agent intent over time.

Approach:

Compare early vs late inputs
Extract keyword intent (e.g., summarize, code, execute)
Detect semantic shift in task direction

### Failure Detection

Detects instability and repeated failures.

Heuristics:

≥ 3 consecutive failures
Failure rate > 50%

### Metrics Computed

Per session:

Total steps
Success vs failure rate
Action distribution

## Design Decisions

### Data Storage Choice

Used: In-memory storage (Python dictionary)

Reasoning:

Fast to implement
No setup overhead
Sufficient for prototype/demo

Trade-off:

Not persistent
Not scalable

### Real-time vs Batch Processing

Used: On-demand processing

Events are stored immediately
Detection is computed when session is queried

Trade-off:

Simpler architecture
Slight delay in insights vs true streaming systems

### Detection Thresholds & Reasoning

Thresholds were chosen to balance:

Avoiding false positives
Detecting meaningful patterns

Examples:

Loop threshold (80%) prevents misclassifying drift as loop
Failure threshold (50%) captures instability without noise

## Trade-offs (Due to Time Constraints)
Used heuristic rules instead of ML/NLP models
Simplified drift detection using keyword matching
In-memory storage instead of database
Minimal UI instead of full-featured dashboard

