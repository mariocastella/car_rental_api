from src.main import app
from fastapi.testclient import TestClient
from fastapi import status

client = TestClient(app)

def test_root_health_check():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "API is running"}