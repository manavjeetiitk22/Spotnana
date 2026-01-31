from collections import defaultdict
from .layover import valid_layover
from .time_utils import local_date_from_utc

def createAdjacencyList(flights_data):
    flights_from = defaultdict(list)
    for flight in flights_data:
        flights_from[flight["origin"]].append(flight)

    return flights_from

def dfs(
    current_airport,
    destination,
    path,
    used_flights,
    results,
    search_date,
    airports_by_code,
    adjacency_list
):
    if current_airport == destination:
        results.append(list(path))
        return

    for flight in adjacency_list[current_airport]:
        if flight["flightNumber"] in used_flights:
            continue

        # Date filter: first flight must depart on requested date
        if not path:
            local_date = local_date_from_utc(
                flight["departure_utc"],
                airports_by_code[flight["origin"]]["timezone"]
            )
            if local_date != search_date:
                continue
        else:
            if not valid_layover(path[-1], flight, airports_by_code):
                continue

        used_flights.add(flight["flightNumber"])

        path.append(flight)

        dfs(
            flight["destination"],
            destination,
            path,
            used_flights,
            results,
            search_date,
            airports_by_code,
            adjacency_list
        )


        path.pop()
        used_flights.remove(flight["flightNumber"])