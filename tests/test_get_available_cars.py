from src.main import app
import pytest
from fastapi.testclient import TestClient
from src.models import Car
from fastapi import status
from datetime import date
from src.storage import get_available_cars
from src.utils import validate_not_past_date

client = TestClient(app)

def test_root_health_check():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "API is running"}

#Unit test
def test_get_available_cars_logic():
    # Simulated data
    cars_list = [
        {"id": 1, "model": "Toyota Corolla"},
        {"id": 2, "model": "Ford Fiesta"},
        {"id": 3, "model": "Honda Civic"},
    ]
    bookings_list = [
        {"car_id": 2, "date": "2026-08-01"},
        {"car_id": 3, "date": "2026-08-02"},
    ]

    request_date = date(2026, 8, 1)

    booked_car_ids = set()
    for booking in bookings_list:
        booking_date = date.fromisoformat(booking["date"])
        if booking_date == request_date:
            booked_car_ids.add(booking["car_id"])

    available_cars = [
        Car(**car) for car in cars_list if car["id"] not in booked_car_ids
    ]

    available_ids = [car.id for car in available_cars]
    assert 2 not in available_ids
    assert set(available_ids) == {1, 3}

#Integration test
def test_get_available_cars_valid_date():
    """Returns available cars on a date where some are booked"""
    response = client.get("/cars/available", params={"request_date": "2026-08-01"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    for car in data:
        Car(**car)
    available_ids = {car["id"] for car in data}
    assert 2 not in available_ids
    assert all(car_id in available_ids for car_id in [1, 3, 4, 5])

def test_get_available_cars_all_booked():
    """Returns an empty list if all cars are booked on the given date"""
    response = client.get("/cars/available", params={"request_date": "2026-08-03"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert data == []  

@pytest.mark.parametrize("invalid_date", [
    "2026/08/01", 
    "01-08-2026",
    "2025-07-30",
    "",
    None
])
def test_get_available_cars_invalid_date(invalid_date):
    """Returns 422 for invalid or missing request_date"""
    params = {} if invalid_date is None else {"request_date": invalid_date}
    response = client.get("/cars/available", params=params)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY