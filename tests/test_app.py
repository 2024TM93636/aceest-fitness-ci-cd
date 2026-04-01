import sys
import os
import pytest

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# ------------------ HOME ------------------

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


# ------------------ MEMBERS ------------------

def test_add_member(client):
    payload = {
        "name": "John",
        "age": 25,
        "plan": "Premium"
    }

    response = client.post("/api/members", json=payload)
    assert response.status_code == 201

    data = response.get_json()
    assert data["name"] == "John"
    assert data["plan"] == "Premium"
    assert "id" in data


def test_get_members(client):
    # Add member first
    client.post("/api/members", json={
        "name": "Alice",
        "age": 28,
        "plan": "Basic"
    })

    response = client.get("/api/members")
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_member_by_id(client):
    response = client.post("/api/members", json={
        "name": "Bob",
        "age": 30,
        "plan": "Gold"
    })

    member = response.get_json()
    member_id = member["id"]

    response = client.get(f"/api/members/{member_id}")
    assert response.status_code == 200

    data = response.get_json()
    assert data["id"] == member_id


def test_update_member(client):
    response = client.post("/api/members", json={
        "name": "Sam",
        "age": 22,
        "plan": "Basic"
    })

    member = response.get_json()
    member_id = member["id"]

    response = client.put(f"/api/members/{member_id}", json={
        "plan": "Premium"
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data["plan"] == "Premium"


def test_delete_member(client):
    response = client.post("/api/members", json={
        "name": "DeleteMe",
        "age": 40,
        "plan": "Basic"
    })

    member = response.get_json()
    member_id = member["id"]

    response = client.delete(f"/api/members/{member_id}")
    assert response.status_code == 200

    response = client.get(f"/api/members/{member_id}")
    assert response.status_code == 404


# ------------------ WORKOUTS ------------------

def test_create_workout(client):
    payload = {
        "title": "Leg Day",
        "difficulty": "Hard"
    }

    response = client.post("/api/workouts", json=payload)
    assert response.status_code == 201

    data = response.get_json()
    assert data["title"] == "Leg Day"


def test_get_workouts(client):
    client.post("/api/workouts", json={
        "title": "Cardio",
        "difficulty": "Easy"
    })

    response = client.get("/api/workouts")
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0


# ------------------ ASSIGN WORKOUT ------------------

def test_assign_workout(client):
    member_res = client.post("/api/members", json={
        "name": "FitUser",
        "age": 27,
        "plan": "Gold"
    })

    workout_res = client.post("/api/workouts", json={
        "title": "HIIT",
        "difficulty": "Medium"
    })

    member_id = member_res.get_json()["id"]
    workout_id = workout_res.get_json()["id"]

    response = client.post(f"/api/members/{member_id}/assign/{workout_id}")
    assert response.status_code == 200

    data = response.get_json()
    assert data["message"] == "Workout assigned"


# ------------------ SEARCH ------------------

def test_search_members(client):
    client.post("/api/members", json={
        "name": "SearchUser",
        "age": 29,
        "plan": "Basic"
    })

    response = client.get("/api/members/search?name=search")
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0