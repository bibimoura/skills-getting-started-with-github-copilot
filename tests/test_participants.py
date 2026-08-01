"""Tests for participants endpoint (DELETE /activities/{activity_name}/participants)"""

import pytest
from fastapi.testclient import TestClient


def test_remove_participant_success(client: TestClient):
    """Test successful removal of a participant from an activity"""
    email = "michael@mergington.edu"  # Already in Chess Club
    
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": email}
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert "Chess Club" in data["message"]
    
    # Verify participant was actually removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities["Chess Club"]["participants"]


def test_remove_participant_nonexistent_activity_returns_404(client: TestClient):
    """Test that removing from nonexistent activity returns 404"""
    response = client.delete(
        "/activities/Nonexistent Activity/participants",
        params={"email": "student@mergington.edu"}
    )
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_remove_nonexistent_participant_returns_404(client: TestClient):
    """Test that removing nonexistent participant returns 404"""
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "nonexistent@mergington.edu"}
    )
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_remove_participant_missing_email_parameter_fails(client: TestClient):
    """Test that removal without email parameter fails"""
    response = client.delete("/activities/Chess Club/participants")
    # Missing required parameter should return 422 (validation error)
    assert response.status_code == 422


def test_remove_participant_empty_email_fails(client: TestClient):
    """Test that removal with empty email fails"""
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": ""}
    )
    # Empty email should fail or return not found
    assert response.status_code in [400, 404, 422]


def test_remove_participant_preserves_other_participants(client: TestClient):
    """Test that removing one participant doesn't remove others"""
    # Get initial participants
    initial_response = client.get("/activities")
    initial_activities = initial_response.json()
    initial_chess_participants = initial_activities["Chess Club"]["participants"].copy()
    
    # Remove one participant
    email_to_remove = "michael@mergington.edu"
    client.delete(
        "/activities/Chess Club/participants",
        params={"email": email_to_remove}
    )
    
    # Get updated participants
    updated_response = client.get("/activities")
    updated_activities = updated_response.json()
    updated_chess_participants = updated_activities["Chess Club"]["participants"]
    
    # Verify the removed participant is gone
    assert email_to_remove not in updated_chess_participants
    
    # Verify other participants remain
    for participant in initial_chess_participants:
        if participant != email_to_remove:
            assert participant in updated_chess_participants
    
    # Should have exactly one fewer participant
    assert len(updated_chess_participants) == len(initial_chess_participants) - 1


def test_remove_participant_twice_fails_second_time(client: TestClient):
    """Test that removing same participant twice fails on second attempt"""
    email = "michael@mergington.edu"
    
    # First removal should succeed
    response1 = client.delete(
        "/activities/Chess Club/participants",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Second removal should fail
    response2 = client.delete(
        "/activities/Chess Club/participants",
        params={"email": email}
    )
    assert response2.status_code == 404


def test_remove_all_participants_one_by_one(client: TestClient):
    """Test removing all participants from an activity"""
    # Get initial participants for an activity
    initial_response = client.get("/activities")
    initial_activities = initial_response.json()
    initial_participants = initial_activities["Music Ensemble"]["participants"].copy()
    
    # Remove each participant
    for email in initial_participants:
        response = client.delete(
            "/activities/Music Ensemble/participants",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Verify all removed
    final_response = client.get("/activities")
    final_activities = final_response.json()
    assert len(final_activities["Music Ensemble"]["participants"]) == 0


def test_remove_participant_response_format(client: TestClient):
    """Test that removal response has correct format"""
    response = client.delete(
        "/activities/Science Club/participants",
        params={"email": "emma@mergington.edu"}
    )
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert isinstance(data["message"], str)
    assert len(data["message"]) > 0


def test_remove_from_different_activities(client: TestClient):
    """Test removing same email from different activities"""
    email = "emma@mergington.edu"  # Already in Programming Class and Science Club
    
    # Remove from Programming Class
    response1 = client.delete(
        "/activities/Programming Class/participants",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Verify still in Science Club
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities["Programming Class"]["participants"]
    assert email in activities["Science Club"]["participants"]
    
    # Remove from Science Club
    response2 = client.delete(
        "/activities/Science Club/participants",
        params={"email": email}
    )
    assert response2.status_code == 200
    
    # Verify removed from both
    final_response = client.get("/activities")
    final_activities = final_response.json()
    assert email not in final_activities["Programming Class"]["participants"]
    assert email not in final_activities["Science Club"]["participants"]
