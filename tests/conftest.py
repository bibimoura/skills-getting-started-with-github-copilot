"""Pytest configuration and shared fixtures for the test suite"""

import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient instance for API testing"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test for proper isolation"""
    # Store initial state
    initial_state = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Team practices and matches against other schools",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 22,
            "participants": ["liam@mergington.edu", "noah@mergington.edu"]
        },
        "Basketball Club": {
            "description": "Pickup games, skills training, and intramural competitions",
            "schedule": "Mondays and Wednesdays, 5:00 PM - 7:00 PM",
            "max_participants": 18,
            "participants": ["ava@mergington.edu", "mia@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore drawing, painting, and mixed media projects",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["sophia@mergington.edu", "isabella@mergington.edu"]
        },
        "Music Ensemble": {
            "description": "Instrumental and vocal ensemble rehearsals and performances",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 30,
            "participants": ["oliver@mergington.edu", "elijah@mergington.edu"]
        },
        "Science Club": {
            "description": "Hands-on experiments, science fairs, and guest lectures",
            "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "lucas@mergington.edu"]
        },
        "Debate Team": {
            "description": "Practice debates, public speaking, and competition preparation",
            "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["grace@mergington.edu", "chloe@mergington.edu"]
        }
    }
    
    # Clear and reset to initial state
    activities.clear()
    activities.update(deepcopy(initial_state))
    
    yield
    
    # Cleanup after test
    activities.clear()
    activities.update(deepcopy(initial_state))
