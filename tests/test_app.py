from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


@pytest.fixture(autouse=True)
def restore_activities():
    original_activities = deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_activities)


def test_root_redirects_to_static_index():
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_details():
    response = client.get("/activities")

    assert response.status_code == 200
    response_activities = response.json()
    assert response_activities.keys() == activities.keys()
    assert response_activities["Chess Club"] == activities["Chess Club"]


def test_signup_adds_participant_and_returns_message():
    email = "new.student@mergington.edu"

    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}
    assert email in activities["Chess Club"]["participants"]


def test_signup_rejects_unknown_activity():
    response = client.post(
        "/activities/Unknown Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_rejects_duplicate_participant():
    email = activities["Chess Club"]["participants"][0]

    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student already signed up for this activity"
    }


def test_signup_rejects_full_activity():
    activity = activities["Chess Club"]
    activity["participants"] = [
        f"student{number}@mergington.edu"
        for number in range(activity["max_participants"])
    ]

    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "new.student@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Activity is full"}


def test_signup_requires_email():
    response = client.post("/activities/Chess Club/signup")

    assert response.status_code == 422


def test_unregister_removes_participant_and_returns_message():
    email = activities["Chess Club"]["participants"][0]

    response = client.delete("/activities/Chess Club/unregister", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Chess Club"}
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_rejects_unknown_activity():
    response = client.delete(
        "/activities/Unknown Club/unregister",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_rejects_unregistered_participant():
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student not signed up for this activity"
    }


def test_unregister_requires_email():
    response = client.delete("/activities/Chess Club/unregister")

    assert response.status_code == 422