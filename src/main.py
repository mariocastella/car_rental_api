# main.py - Entry point for the Car Rental API
# Sets up FastAPI app and logging configuration and data reset
from fastapi import FastAPI
import logging
from src.routes import router
import shutil
from pathlib import Path

# Configure logging to file
logging.basicConfig(
    filename="car_rental.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# Reset data file to original state before starting the app
def reset_data_file():
    original = Path(__file__).parent.parent / "data" / "data_original.json"
    target = Path(__file__).parent.parent / "data" / "data.json"
    shutil.copyfile(original, target)

reset_data_file()

app = FastAPI(
    title="Car Rental API",
    version="0.1.0",
    description="This API provides endpoints to manage car rentals, including listing available cars and creating bookings."
)

# Register API routes
app.include_router(router)

@app.get("/")
def root():
    """Health check endpoint."""
    return {"message": "API is running"}