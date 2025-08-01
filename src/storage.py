# storage.py - Data access functions for Car Rental API
import json
import logging
from pathlib import Path
from datetime import date
from .models import Car

# Path to the JSON data file
DATA_FILE = Path(__file__).parent.parent / "data" / "data.json"

def load_data():
    """
    Load the JSON data file and return its content as a dictionary.
    """
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            cars = data.get("cars", [])
            bookings = data.get("bookings", [])
            return cars, bookings
    except Exception as e:
        logging.error(f"Error loading data file {DATA_FILE}: {e}")
        raise

def get_available_cars(request_date: date) -> list[Car]:
    """
    Get list of cars available for rental on a specific date.
    
    Args:
        request_date: Date to check availability
    
    Returns:
        List of available cars
    """
    cars_list, bookings_list = load_data()
    
    # Create set of car IDs that are booked on the requested date
    booked_car_ids = set()
    for booking in bookings_list:
        booking_date = date.fromisoformat(booking["date"])  # Convert string to date object
        if booking_date == request_date:
            booked_car_ids.add(booking["car_id"])
    
    logging.debug(f"Found {len(booked_car_ids)} booked cars on {request_date}")
    
    # Filter cars that are not booked and convert to Car objects
    available_cars = [
        Car(**car) for car in cars_list 
        if car["id"] not in booked_car_ids
    ]
    
    logging.info(f"Available cars query: {len(available_cars)}/{len(cars_list)} cars available on {request_date}")
    
    return available_cars