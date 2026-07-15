from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "student@example.com"

    signup_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert signup_response.status_code == 200

    delete_response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})
    assert delete_response.status_code == 200

    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_participant_returns_404_when_not_found():
    response = client.delete("/activities/Chess Club/signup", params={"email": "missing@example.com"})
    assert response.status_code == 404
