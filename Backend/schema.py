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

class Layover(BaseModel):
    airport: str
    duration_minutes: int
    duration_human: str

class Itinerary(BaseModel):
    flights: List[Flight]
    layovers: List[Layover]
    total_price: float