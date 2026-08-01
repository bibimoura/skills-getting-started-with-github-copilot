"""Tests for activities endpoints (GET / and GET /activities)"""

import pytest
from fastapi.testclient import TestClient


def test_root_redirects_to_static_index(client: TestClient):
    """Test that GET / redirects to /static/index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_all_activities_returns_dict(client: TestClient):
    """Test that GET /activities returns all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 9  # 9 activities total


def test_get_all_activities_has_required_fields(client: TestClient):
    """Test that each activity has required fields"""
    response = client.get("/activities")
    data = response.json()
    
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    for activity_name, activity_data in data.items():
        assert isinstance(activity_name, str)
        assert len(activity_name) > 0
        
        assert isinstance(activity_data, dict)
        assert required_fields.issubset(activity_data.keys())
        
        # Validate field types
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)
        
        # Participants should be list of strings (emails)
        for participant in activity_data["participants"]:
            assert isinstance(participant, str)
            assert "@" in participant


def test_get_all_activities_contains_expected_activities(client: TestClient):
    """Test that the response contains expected activities"""
    response = client.get("/activities")
    data = response.json()
    
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Soccer Team",
        "Basketball Club",
        "Art Club",
        "Music Ensemble",
        "Science Club",
        "Debate Team"
    ]
    
    for activity in expected_activities:
        assert activity in data


def test_get_activities_chess_club_details(client: TestClient):
    """Test specific activity details - Chess Club"""
    response = client.get("/activities")
    data = response.json()
    
    chess = data["Chess Club"]
    assert chess["description"] == "Learn strategies and compete in chess tournaments"
    assert chess["schedule"] == "Fridays, 3:30 PM - 5:00 PM"
    assert chess["max_participants"] == 12
    assert "michael@mergington.edu" in chess["participants"]
    assert "daniel@mergington.edu" in chess["participants"]


def test_get_activities_programming_class_details(client: TestClient):
    """Test specific activity details - Programming Class"""
    response = client.get("/activities")
    data = response.json()
    
    programming = data["Programming Class"]
    assert programming["description"] == "Learn programming fundamentals and build software projects"
    assert programming["schedule"] == "Tuesdays and Thursdays, 3:30 PM - 4:30 PM"
    assert programming["max_participants"] == 20
    assert "emma@mergington.edu" in programming["participants"]


def test_activities_have_initial_participants(client: TestClient):
    """Test that activities have pre-populated participants"""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity_data in data.items():
        assert len(activity_data["participants"]) > 0, f"{activity_name} should have initial participants"


def test_participants_are_valid_emails(client: TestClient):
    """Test that all participants have valid email format"""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity_data in data.items():
        for email in activity_data["participants"]:
            assert "@" in email, f"Invalid email format: {email}"
            assert email.endswith("@mergington.edu"), f"Email should be from mergington.edu: {email}"
