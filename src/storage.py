# storage.py - Data access functions for Car Rental API
import json
import logging
from pathlib import Path
from .models import Car, Booking

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