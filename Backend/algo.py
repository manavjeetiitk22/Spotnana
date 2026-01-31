import json
from datetime import datetime
from zoneinfo import ZoneInfo
from collections import defaultdict
from datetime import timedelta

def load_airports(path="flights.json"):
    with open(path, 'r') as file:
        data = json.load(file) 
    
    airports_by_code = {}

    for airport in data['airports']:
        key = airport['code']
        value = airport
        airports_by_code[key] = value

    return airports_by_code


def load_flights(path="flights.json"):
    with open(path, 'r') as file:
        data = json.load(file)

    return data["flights"]

airports_by_code = load_airports()
flights_data = load_flights()  

# print(airports_by_code)
# print(flights_data)

def to_utc(local_time_str, airport_code):

    # airports_by_code = load_airports()
    tz = ZoneInfo(airports_by_code[airport_code]["timezone"])
    local_dt = datetime.fromisoformat(local_time_str).replace(tzinfo=tz)
    return local_dt.astimezone(ZoneInfo("UTC"))

def flights_time_to_utc():

    for flight in flights_data:
        flight["departure_utc"] = to_utc(flight["departureTime"], flight["origin"])
        flight["arrival_utc"]   = to_utc(flight["arrivalTime"], flight["destination"])

    return flights_data

def createAdjacencyList(flights_data):
    flights_from = defaultdict(list)
    for flight in flights_data:
        flights_from[flight["origin"]].append(flight)

    return flights_from

flights_data_utc = flights_time_to_utc()
adjacency_list = createAdjacencyList(flights_data_utc)

# print(adjacency_list)

def is_domestic(prev_flight, next_flight):
    country1 = airports_by_code[prev_flight["destination"]]["country"]
    country2 = airports_by_code[next_flight["origin"]]["country"]
    return country1 == country2



MIN_DOMESTIC = timedelta(minutes=45)
MIN_INTERNATIONAL = timedelta(minutes=90)
MAX_LAYOVER = timedelta(hours=6)

def valid_layover(prev_flight, next_flight):
    # airport change not allowed
    if prev_flight["destination"] != next_flight["origin"]:
        return False

    layover = next_flight["departure_utc"] - prev_flight["arrival_utc"]

    if layover < timedelta(0):
        return False

    min_required = (
        MIN_DOMESTIC if is_domestic(prev_flight, next_flight)
        else MIN_INTERNATIONAL
    )

    return min_required <= layover <= MAX_LAYOVER


def dfs(current_airport, destination, path, used_flights, results, search_date="2024-03-15"):
    print(f"DFS at {current_airport}, path length: {len(path)}")

    if current_airport == destination and path:
        results.append(path.copy())
        return

    # Stop if too many flights
    if len(path) >= 3:
        return
        
    # print(adjacency_list[current_airport])
    for flight in adjacency_list[current_airport]:
        print(f"Considering flight {flight['flightNumber']} from {flight['origin']} to {flight['destination']}")
        if flight["flightNumber"] in used_flights:
            continue

        # Date filter: first flight must depart on requested date
        if not path:
            local_date = (
                flight["departure_utc"]
                .astimezone(
                    ZoneInfo(airports_by_code[flight["origin"]]["timezone"])
                )
                .date()
                .isoformat()
            )

            if local_date != search_date:
                continue
        else:
            if not valid_layover(path[-1], flight):
                continue

        # used_flights.add(flight)
        used_flights.add(flight["flightNumber"])

        path.append(flight)

        dfs(
            flight["destination"],
            destination,
            path,
            used_flights,
            results,
            search_date
        )


        path.pop()
        used_flights.remove(flight["flightNumber"])

def search_itineraries(source, destination, date):
    if source not in airports_by_code or destination not in airports_by_code:
        print('Invalid source or destination airport code.')
        return []

    print(f"Searching itineraries from {source} to {destination} on {date}...")
    results = []
    dfs(
        current_airport=source,
        destination=destination,
        path=[],
        used_flights=set(),
        results=results,
        search_date=date
    )
    return results

def format_duration(td):
    total_minutes = int(td.total_seconds() // 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours}h {minutes}m"

def compute_layovers_with_airports(path):
    layovers = []
    for i in range(len(path) - 1):
        layover_duration = (
            path[i + 1]["departure_utc"] - path[i]["arrival_utc"]
        )
        layovers.append({
            "airport": path[i]["destination"],
            "duration": layover_duration
        })
    return layovers

def print_itineraries(itineraries):
    for idx, itinerary in enumerate(itineraries, 1):
        print(f"\nItinerary {idx} ({len(itinerary)-1} stop{'s' if len(itinerary)-1 != 1 else ''})")

        route = " → ".join(
            [itinerary[0]["origin"]] +
            [f["destination"] for f in itinerary]
        )
        print(f"Route: {route}")

        total_price = 0

        for i, flight in enumerate(itinerary):
            price = float(flight["price"])
            total_price += price

            print(
                f"  {flight['flightNumber']} | "
                f"{flight['origin']} → {flight['destination']} | "
                f"${price}"
            )

            if i < len(itinerary) - 1:
                layover = (
                    itinerary[i + 1]["departure_utc"]
                    - flight["arrival_utc"]
                )
                print(
                    f"    Layover at {flight['destination']}: "
                    f"{format_duration(layover)}"
                )

        print(f"Total price: ${total_price}")
        print("-" * 50)

results = search_itineraries("SFO", "NRT", "2024-03-15")
print_itineraries(results)
print(len(results))