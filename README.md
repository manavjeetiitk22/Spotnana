# SkyPath – Flight Connection Search Engine

This project is a simple flight connection search engine with:
- **Backend**: FastAPI (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Containerization**: Docker + Docker Compose

Users can search for valid flight itineraries by providing:
- Origin
- Destination
- Date

## Running the Project Using Docker (Recommended)

### Prerequisites
- Docker
- Docker Compose

### Steps

1. Clone the repository
`git clone <repo-url>`
`cd Spotnana`

2. Build and start services
`docker compose up --build`

3. Access the application
- Frontend: `http://localhost:8080`
- Backend API: `http://localhost:8000`

---

## Running the Project Locally (Without Docker)

### Backend (FastAPI)

#### Prerequisites
- Python 3.10+
- pip

1. Navigate to backend 
`cd Backend`
2. Install dependencies 
`pip install -r requirements.txt`
3. Start the backend server
`uvicorn main:app --reload`

### Test Backend Directly
http://localhost:8000/search?origin=SFO&destination=NRT&date=2024-03-15


## Features

- Search valid flight itineraries between origin and destination
- Supports:
  - Direct and multi-leg flights (up to 3 flights / 2 layovers)
  - Domestic and international layover rules
  - Time-zone aware date filtering
- Returns:
  - Complete flight sequences
  - Layover durations at each connection
  - Total price and total travel time
- Simple frontend for querying and visualizing itineraries

---


## Core Design Decisions

### 1. Flights as a Graph

The flight network is modeled as a **directed graph**:

- **Nodes** → Airports  
- **Edges** → Flights (with time, price, metadata)

An adjacency list maps each airport to its outgoing flights.

**Why a graph?**
- Flight search is naturally a path-finding problem
- Connections, cycles, and layovers map cleanly to traversal logic
- Enables clear constraint enforcement during search

---

### 2. DFS-Based Itinerary Search

The search algorithm uses **Depth-First Search (DFS)** to enumerate all valid itineraries.

**Why DFS?**
- The goal is to find **all valid itineraries**, not just the cheapest or shortest
- DFS allows:
  - Hard stop limits (max 3 flights)
  - Early pruning of invalid paths
  - Clean enforcement of domain rules

**Constraints enforced during DFS**
- Maximum flights (≤ 3)
- No repeated flights (cycle prevention)
- Valid layover duration
- First flight must depart on the requested date (local time)

This keeps the algorithm correct and explainable.

---

### 3. Time Handling Strategy

Time handling follows a strict rule:

- **All calculations → UTC**
- **All date comparisons → local airport time**

Each flight’s local time is converted to UTC at ingestion.

**Why this matters**
- Prevents bugs caused by:
  - International date line crossings
  - Late-night departures
  - Mixed timezone arithmetic

**Key lesson**
> Dates are local concepts. Times are global (UTC) concepts.

---

### 4. Layover Validation

Layovers are validated using `datetime.timedelta` for clarity and type safety:

```python
MIN_DOMESTIC = timedelta(minutes=45)
MIN_INTERNATIONAL = timedelta(minutes=90)
MAX_LAYOVER = timedelta(hours=6)
```
This avoids unit ambiguity and ensures correct datetime arithmetic.

### 4. Backend–Frontend Separation
Backend (FastAPI):
- Search logic
- Time handling
- Itinerary construction

Frontend (HTML/JS):
- User input
- Sorting and rendering
- Presentation of layovers and travel time

### Tradeoffs Considered
DFS vs Shortest-Path 

| Algorithm | Reason Not Chosen |
|---------|------------------|
| Dijkstra | Optimizes a single metric (e.g., cost or time); does not account all valid itineraries |
| A* | Adds unnecessary complexity for an early-stage prototype |

### What I Would Improve With More Time
1. Smarter Algorithms
- Implement Dijkstra / A* for: Cheapest itinerary, Fastest itinerary
- Multi-objective optimization (price + time + stops)
Dominance-based pruning
2. UI Enhancements: 
- Expand/collapse per itinerary
- Sorting dropdown (Price / Duration / Stops)
3. Performance & Scale
- Memoization of subpaths
- Top-K itinerary limiting

