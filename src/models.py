# models.py - Pydantic models for Car Rental API
from pydantic import BaseModel
from datetime import date

class Car(BaseModel):
    """Represents a car available for rental."""
    id: int
    model: str

class Booking(BaseModel):
    """Represents a booking for a car on a specific date."""
    car_id: int
    date: date