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

