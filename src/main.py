# main.py - Entry point for the Car Rental API
# Sets up FastAPI app and logging configuration and data reset
from fastapi import FastAPI
import logging

# Configure logging to file
logging.basicConfig(
    filename="car_rental.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

app = FastAPI(
    title="Car Rental API",
    version="0.1.0",
    description="This API provides endpoints to manage car rentals, including listing available cars and creating bookings."
)

@app.get("/")
def root():
    """Health check endpoint."""
    return {"message": "API is running"}