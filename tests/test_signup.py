"""Tests for signup endpoint (POST /activities/{activity_name}/signup)"""

import pytest
from fastapi.testclient import TestClient


def test_signup_success(client: TestClient):
    """Test successful signup for an activity"""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]
    
    # Verify student was actually added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_multiple_activities(client: TestClient):
    """Test that a student can signup for multiple different activities"""
    student_email = "multistudent@mergington.edu"
    
    # Signup for first activity
    response1 = client.post(
        "/activities/Chess Club/signup",
        params={"email": student_email}
    )
    assert response1.status_code == 200
    
    # Signup for second activity
    response2 = client.post(
        "/activities/Programming Class/signup",
        params={"email": student_email}
    )
    assert response2.status_code == 200
    
    # Verify signup in both
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert student_email in activities["Chess Club"]["participants"]
    assert student_email in activities["Programming Class"]["participants"]


def test_signup_duplicate_fails(client: TestClient):
    """Test that duplicate signup for same activity fails"""
    email = "michael@mergington.edu"  # Already in Chess Club
    
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower()


def test_signup_nonexistent_activity_returns_404(client: TestClient):
    """Test that signup for nonexistent activity returns 404"""
    response = client.post(
        "/activities/Nonexistent Activity/signup",
        params={"email": "student@mergington.edu"}
    )
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_signup_empty_email_succeeds(client: TestClient):
    """Test that signup with empty email is accepted (no validation)"""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": ""}
    )
    # App doesn't validate email format, so empty string is accepted
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    
    # Verify empty email was added to participants
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "" in activities["Chess Club"]["participants"]


def test_signup_missing_email_parameter_fails(client: TestClient):
    """Test that signup without email parameter fails"""
    response = client.post("/activities/Chess Club/signup")
    # Missing required parameter should return 422 (validation error)
    assert response.status_code == 422


def test_signup_all_activities_accessible(client: TestClient):
    """Test that we can signup for all existing activities"""
    test_email = "versatile@mergington.edu"
    
    activities_response = client.get("/activities")
    activities = activities_response.json()
    activity_names = list(activities.keys())
    
    # Try to signup for each activity
    for activity_name in activity_names:
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )
        assert response.status_code == 200, f"Failed to signup for {activity_name}"


def test_signup_response_format(client: TestClient):
    """Test that signup response has correct format"""
    response = client.post(
        "/activities/Art Club/signup",
        params={"email": "artist@mergington.edu"}
    )
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert isinstance(data["message"], str)
    assert len(data["message"]) > 0


def test_signup_preserves_existing_participants(client: TestClient):
    """Test that adding a new participant doesn't remove existing ones"""
    # Get initial participants
    initial_response = client.get("/activities")
    initial_activities = initial_response.json()
    initial_chess_participants = initial_activities["Chess Club"]["participants"].copy()
    
    # Add new participant
    client.post(
        "/activities/Chess Club/signup",
        params={"email": "newmember@mergington.edu"}
    )
    
    # Get updated participants
    updated_response = client.get("/activities")
    updated_activities = updated_response.json()
    updated_chess_participants = updated_activities["Chess Club"]["participants"]
    
    # Verify all initial participants are still there
    for original_participant in initial_chess_participants:
        assert original_participant in updated_chess_participants
    
    # Verify new participant was added
    assert "newmember@mergington.edu" in updated_chess_participants
    # Should have exactly one more participant
    assert len(updated_chess_participants) == len(initial_chess_participants) + 1
