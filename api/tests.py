import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_hello_world():
    client = APIClient()
    response = client.get("/api/hello/")
    assert response.status_code == 200
    assert response.data["message"] == "Hello from Django REST API!"
