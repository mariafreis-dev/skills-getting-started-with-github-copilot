from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "student@example.com"

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    delete_response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    assert delete_response.status_code == 200

    activities = activities_response.json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_participant_returns_404_when_not_found():
    # Arrange
    activity_name = "Chess Club"
    email = "missing@example.com"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
