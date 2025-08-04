from src.main import app
import pytest
from fastapi.testclient import TestClient
from src.models import Booking
from fastapi import status
from src.storage import DATA_FILE
import json
from datetime import date
from src.exceptions import CarNotFoundError, CarAlreadyBookedError

client = TestClient(app)

def test_root_health_check():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "API is running"}

#Unitary test for booking creation
cars_list = [
    {"id": 1, "model": "Toyota Corolla"},
    {"id": 2, "model": "Ford Fiesta"},
]

bookings_list = [
    {"car_id": 1, "date": "2026-08-01"},
]

def validate_booking_logic(new_booking: Booking, cars, bookings):
    if not any(car["id"] == new_booking.car_id for car in cars):
        return "car_not_found"
    if any(b["car_id"] == new_booking.car_id and b["date"] == new_booking.date.isoformat() for b in bookings):
        return "car_already_booked"
    return "ok"

def test_booking_logic_car_not_found():
    booking = Booking(car_id=99, date=date(2026, 8, 1))
    result = validate_booking_logic(booking, cars_list, bookings_list)
    assert result == "car_not_found"

def test_booking_logic_car_already_booked():
    booking = Booking(car_id=1, date=date(2026, 8, 1))
    result = validate_booking_logic(booking, cars_list, bookings_list)
    assert result == "car_already_booked"

def test_booking_logic_ok():
    booking = Booking(car_id=2, date=date(2026, 8, 2))
    result = validate_booking_logic(booking, cars_list, bookings_list)
    assert result == "ok"
    
# Integration test for booking creation
def test_post_succes_booking():
    """Creates a booking and checks it's appended in bookings data file"""
    new_booking = {"car_id": 1, "date": "2026-09-06"}
    response = client.post("/bookings/", json=new_booking)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == new_booking
    
    Booking(**response.json())

    with open(DATA_FILE, encoding="utf-8") as f:
        data = json.load(f)

    assert data["bookings"][-1] == new_booking

def test_post_booking_car_not_found():
    """Check returns 404 if car ID does not exist"""
    response = client.post("/bookings/", json={
        "car_id": 99,
        "date": "2026-08-05"
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Car ID 99 not found"}


def test_create_booking_already_booked():
    """Check returns 409 if car is already booked on that date"""
    response = client.post("/bookings/", json={
        "car_id": 2,
        "date": "2026-08-01"
    })
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {"detail": "Car ID 2 already booked on 2026-08-01"}


@pytest.mark.parametrize("payload", [
    {},  # Missing both fields
    {"car_id": 1},  # Missing date
    {"date": "2026-08-01"},  # Missing car_id
    {"car_id": "a", "date": "2026-08-01"},  # Invalid car_id
    {"car_id": 1, "date": "not-a-date"},  # Invalid date
    {"car_id": 1, "date": "2025-07-30"}  # Past date
])
def test_post_booking_invalid_payload(payload):
    """Check returns 422 for invalid payloads"""
    response = client.post("/bookings/", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY