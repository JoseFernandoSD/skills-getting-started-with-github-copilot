import copy

from fastapi.testclient import TestClient

import src.app as app_module


client = TestClient(app_module.app)
INITIAL_ACTIVITIES = copy.deepcopy(app_module.activities)


def reset_activities():
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(INITIAL_ACTIVITIES))


def test_unregister_removes_participant():
    reset_activities()

    signup_response = client.post(
        "/activities/Chess%20Club/signup?email=test@example.edu"
    )
    assert signup_response.status_code == 200

    delete_response = client.delete(
        "/activities/Chess%20Club/signup?email=test@example.edu"
    )

    assert delete_response.status_code == 200
    assert delete_response.json() == {
        "message": "Unregistered test@example.edu from Chess Club"
    }

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    assert "test@example.edu" not in activities_response.json()["Chess Club"]["participants"]


def test_unregister_unknown_participant_returns_404():
    reset_activities()

    delete_response = client.delete(
        "/activities/Chess%20Club/signup?email=missing@example.edu"
    )

    assert delete_response.status_code == 404
    assert delete_response.json()["detail"] == "Participant not found"
