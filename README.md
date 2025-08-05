# Car Rental API

A minimal yet robust REST API for a car rental service, built with **FastAPI** and **JSON-based file storage**.

## Features

- List available cars for a specific date
- Create bookings for cars
- File-based storage (JSON)
- Comprehensive logging
- Interactive API documentation

## Installation

### Prerequisites

- Python 3.11 or higher
- Poetry (for dependency management)

If you don't have Poetry installed, install it with:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
Use `python`, `py`, or `python3` according to your Python installation.

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd car_rental_api
```

2. Install dependencies:
```bash
poetry install
```

## Usage

### Running the API

Start the development server:
```bash
poetry run uvicorn src.main:app --reload
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive Documentation**: http://localhost:8000/docs
- **Alternative Documentation**: http://localhost:8000/redoc

### API Endpoints

#### List Available Cars
```
GET /cars/available?date=YYYY-MM-DD
```
Returns a list of cars available for rental on the specified date.

Example:
```Bash
curl 'http://localhost:8000/cars/available?date=2026-08-01'
````
Responses: 
- 200 OK → Success
- 422 Unprocessable Entity → Invalid input or past date

#### Create a Booking
```
POST /bookings/
Content-Type: application/json
```
Creates a new booking for a car on a specific date.

Example:
```Bash
curl -X POST http://localhost:8000/bookings/ \
  -H "Content-Type: application/json" \
  -d '{"car_id": 3, "date": "2026-08-15"}'
```
Responses:

- 201 Created → Success
- 404 Not Found → Car does not exist
- 409 Conflict → Car already booked
- 422 Unprocessable Entity → Invalid input or past date

## Project Structure

```
car_rental/
├── data/
│   ├── data.json           # Runtime data
│   └── data_original.json  # Reset state
├── src/
│   ├── main.py             # FastAPI application entry point
│   ├── models.py           # Pydantic schemas
│   ├── routes.py           # Endpoints
│   ├── storage.py          # Data logic
│   ├── utils.py            # Validation helpers
│   └── exceptions.py       # Custom exceptions
├── tests/
│   ├── test_get_available_cars.py
│   └── test_post_booking.py
├── pyproject.toml          # Poetry project config
└── README.md
```

## Design Choices

### Architecture
- **FastAPI**: Chosen for its modern async support, automatic documentation, and type safety
- **Pydantic Models**: For data validation and serialization
- **File-based Storage**: JSON file for simplicity as specified in requirements
- **Modular Structure**: Separated concerns into different modules (models, routes, storage)

### Data Storage
- Using JSON file storage for simplicity
- Data structure includes `cars` and `bookings` arrays

### Logging
- Configured to log to `car_rental.log` file
- Captures key application events (queries, bookings)
- Uses standard Python logging module

## Testing

Run the tests:
```bash
poetry run pytest
```

## Development

### Adding New Features
1. Update models in `models.py` if needed
2. Add endpoints in `routes.py`
3. Update `data.json` and storage functions in `storage.py` if required
4. Add tests in `tests/` directory

### Logging
The application logs important events to `car_rental.log`:
- Successful and failed booking attempts
- Queries for available cars
- Application startup and errors

## Future Enhancements

 **Full Asynchronous Support:** Convert all API operations and file I/O to async for better performance and scalability.
- **NoSQL Database:** Replace the JSON file storage with a NoSQL database (e.g., MongoDB) to better handle larger data volumes and concurrency.
Testing strategy
- **Testing strategy:** 
Refactor tests to clearly separate unit and integration tests. Use unittest.mock or pytest-mock to isolate logic from file I/O and API behavior. Expand test coverage to include negative cases and edge conditions.
- **Automated Testing with CI/CD:** Set up GitHub Actions (YAML workflow) or other CI pipelines to automatically run tests on every push or pull request.
- **Bookings with Date Ranges:** Allow bookings that span multiple days (start date to end date) instead of only single-day reservations.
- **Expanded Data Models:**  
  - **Cars:** Add fields like brand, year, type (SUV, sedan), daily price, features (AC, GPS, etc.)  
  - **Bookings:** Include customer information (name, email), booking status (confirmed, canceled), payment methods, timestamps.
- **Additional Endpoints:**  
  - Query bookings by car, customer, or date range  
  - Cancel or modify bookings  
  - Usage and revenue statistics per car or period
- **Authentication & Authorization:** Add security layers using OAuth2 or JWT, so only authenticated users can create bookings or access sensitive data.
- **Enhanced Documentation:** Provide richer Swagger examples, tutorials, and developer guides.
- **Containerization:** Provide full Docker support with Dockerfiles and docker-compose for easy deployment.

## License

All rights reserved.

## Author

Mario Castella - mariocast124@gmail.com
