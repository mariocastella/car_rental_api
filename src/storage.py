# storage.py - Data access functions for Car Rental API
import json
import logging
from pathlib import Path
from datetime import date
from .models import Car, Booking
from .exceptions import CarNotFoundError, CarAlreadyBookedError

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

def create_booking(new_booking: Booking) -> Booking:
    """
    Create a new booking for a car on a specific date.

    Args:
        new_booking (Booking): Booking object containing car_id and date.

    Returns:
        Booking: The created booking.

    Raises:
        CarNotFoundError: If the car does not exist.
        CarAlreadyBookedError: If the car is already booked on that date.
    """

    cars_list, bookings_list = load_data()

    # Check if the car exists
    if not any(car["id"] == new_booking.car_id for car in cars_list):
        raise CarNotFoundError(f"Car ID {new_booking.car_id} not found")

    # Check if the car is already booked on the requested date
    if any(
        booking["car_id"] == new_booking.car_id and
        booking["date"] == new_booking.date.isoformat()
        for booking in bookings_list
    ):
        raise CarAlreadyBookedError(f"Car ID {new_booking.car_id} already booked on {new_booking.date}")

    bookings_list.append({
        "car_id": new_booking.car_id,
        "date": new_booking.date.isoformat()
    })

    new_data = {
        "cars": cars_list,
        "bookings": bookings_list
    }

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=1)

    logging.info(f"Booking created: car_id={new_booking.car_id}, date={new_booking.date}")

    return new_booking