from unittest.mock import MagicMock, patch

import pytest

from app.database.models import User
from app.services.auth import auth_service


@pytest.fixture()
def token(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("app.routes.auth.send_email", mock_send_email)
    client.post("/api/auth/signup", json=user)
    current_user: User = (
        session.query(User).filter(User.email == user.get("email")).first()
    )
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": user.get("password")},
    )
    data = response.json()
    return data["access_token"]


def test_create_tag(client, token):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        response = client.post(
            "/api/photos/new/",
            json={
                "title": input("test_title"),
                "description": input("test_description"),
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["title"] == "test_title"
        assert data["description"] == "test_description"
        assert "id" in data
