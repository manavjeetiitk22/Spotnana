from datetime import timedelta

def is_domestic(prev_flight, next_flight,airports_by_code):
    country1 = airports_by_code[prev_flight["destination"]]["country"]
    country2 = airports_by_code[next_flight["origin"]]["country"]
    return country1 == country2

MIN_DOMESTIC = timedelta(minutes=45) 
MIN_INTERNATIONAL = timedelta(minutes=90)
MAX_LAYOVER = timedelta(hours=6)

def valid_layover(prev_flight, next_flight, airports_by_code):
    # airport change not allowed
    if prev_flight["destination"] != next_flight["origin"]:
        return False

    layover = next_flight["departure_utc"] - prev_flight["arrival_utc"]

    if layover < timedelta(0):
        return False

    min_required = (
        MIN_DOMESTIC if is_domestic(prev_flight, next_flight, airports_by_code)
        else MIN_INTERNATIONAL
    )

    return min_required <= layover <= MAX_LAYOVER