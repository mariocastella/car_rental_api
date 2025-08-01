# routes.py - API route definitions for Car Rental API
from fastapi import APIRouter
from .models import Car, Booking

# Create API router
router = APIRouter()

@router.get("/cars/available", 
    response_model=list[Car],
    summary="List available cars for a specific date",
    description="Returns a list of cars that are not booked on the provided date (YYYY-MM-DD). Assuming that for dates in the past, no cars are available.")
def get_available_cars_endpoint(request_date: date):


@router.post("/bookings/", 
    response_model=Booking, 
    status_code=201,
    summary="Create a new car booking",
    description="Create a new booking for a car on a specific date. Assuming that can not book a car on a past date.")
def create_booking_endpoint(new_booking: Booking):