from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .data_loader import load_airports, load_flights
from .time_utils import to_utc,format_layover
from .search import dfs, createAdjacencyList
from typing import List
from .schema import Flight, Itinerary

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# data = load_data()
airports_by_code = load_airports()
flights_data = load_flights()

for f in flights_data:
    f["departure_utc"] = to_utc(
        f["departureTime"],
        airports_by_code[f["origin"]]["timezone"]
    )
    f["arrival_utc"] = to_utc(
        f["arrivalTime"],
        airports_by_code[f["destination"]]["timezone"]
    )

adjacency_list = createAdjacencyList(flights_data)

@app.get("/search", response_model=List[Itinerary])
def search_flights(origin: str, destination: str, date: str):
    results = []
    dfs(
        origin,
        destination,
        [],
        set(),
        results,
        date,
        airports_by_code,
        adjacency_list
    )

    response = []
    for path in results:
        flight_objs = []
        layovers = []

        for i, f in enumerate(path):
            flight_objs.append(
                Flight(
                    flightNumber=f["flightNumber"],
                    origin=f["origin"],
                    destination=f["destination"],
                    departureTime=f["departureTime"],
                    arrivalTime=f["arrivalTime"],
                    price=float(f["price"]),
                    aircraft=f["aircraft"]
                )
            )

            # Add layover after this flight (if not last)
            if i < len(path) - 1:
                layover_td = path[i + 1]["departure_utc"] - f["arrival_utc"]
                minutes = int(layover_td.total_seconds() // 60)

                layovers.append({
                    "airport": f["destination"],
                    "duration_minutes": minutes,
                    "duration_human": format_layover(layover_td)
                })

        response.append(
            Itinerary(
                flights=flight_objs,
                layovers=layovers,
                total_price=sum(f.price for f in flight_objs)
            )
        )

    return response