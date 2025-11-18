import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_success():
    response = client.post("/activities/Chess Club/signup?email=tester@mergington.edu")
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    # Clean up: remove the test participant
    client.delete("/activities/Chess Club/unregister?email=tester@mergington.edu")

def test_signup_duplicate():
    email = "michael@mergington.edu"
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_full():
    # Fill up the activity
    activity = "Math Olympiad"
    for i in range(25 - 2):
        client.post(f"/activities/{activity}/signup?email=fulltest{i}@mergington.edu")
    # Now it should be full
    response = client.post(f"/activities/{activity}/signup?email=overflow@mergington.edu")
    assert response.status_code == 400
    assert "Activity is full" in response.json()["detail"]
    # Clean up
    for i in range(25 - 2):
        client.delete(f"/activities/{activity}/unregister?email=fulltest{i}@mergington.edu")

def test_unregister():
    # Add, then remove
    email = "toremove@mergington.edu"
    client.post(f"/activities/Art Club/signup?email={email}")
    response = client.delete(f"/activities/Art Club/unregister?email={email}")
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
