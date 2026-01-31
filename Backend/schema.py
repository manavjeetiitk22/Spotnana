from pydantic import BaseModel
from typing import List

class Flight(BaseModel):
    flightNumber: str
    origin: str
    destination: str
    departureTime: str
    arrivalTime: str
    price: float
    aircraft: str

class Itinerary(BaseModel):
    flights: List[Flight]
    total_price: float