# routes.py - API route definitions for Car Rental API
from fastapi import APIRouter
from .models import Car, Booking
from datetime import date
from .storage import get_available_cars
from .utils import validate_not_past_date

# Create API router
router = APIRouter()

@router.get(
    "/cars/available", 
    response_model=list[Car],
    summary="List available cars for a specific date",
    description="Returns a list of cars that are not booked on the provided date (YYYY-MM-DD). Assuming that for dates in the past, no cars are available.")
def get_available_cars_endpoint(request_date: date):
    """
    Get list of cars available for rental on a specific date.
    """
    validate_not_past_date(request_date)
    return get_available_cars(request_date)
