import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Tennis Club" in data

def test_signup_and_unregister():
    # Use a unique email to avoid conflicts
    activity = "Tennis Club"
    email = "pytestuser@mergington.edu"

    # Ensure not already registered
    client.delete(f"/activities/{activity}/unregister?email={email}")

    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]

    # Duplicate signup should fail
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400

    # Unregister
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert f"Unregistered {email}" in response.json()["message"]

    # Unregister again should fail
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 404


def test_signup_invalid_activity():
    response = client.post("/activities/NonexistentActivity/signup?email=foo@bar.com")
    assert response.status_code == 404


def test_unregister_invalid_activity():
    response = client.delete("/activities/NonexistentActivity/unregister?email=foo@bar.com")
    assert response.status_code == 404


def test_signup_already_registered():
    activity = "Tennis Club"
    email = "alex@mergington.edu"  # Already registered in initial data
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
