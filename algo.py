import json

def load_airports(path="flights.json"):
    with open(path, 'r') as file:
        data = json.load(file) 
    
    airports_by_code = {}

    for airport in data['airports']:
        key = airport['code']
        value = airport
        airports_by_code[key] = value

    return airports_by_code

airports_by_code = load_airports()

# print(airports_by_code)


