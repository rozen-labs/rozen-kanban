import pytest
from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()


@pytest.mark.django_db
def test_registration_logs_in_and_redirects_to_dashboard():
    client = Client()
    response = client.post(
        "/accounts/register/",
        {
            "username": "newuser",
            "email": "newuser@example.com",
            "role": User.Role.DEVELOPER,
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
        },
    )
    assert response.status_code == 302
    assert response.url == "/"

    user = User.objects.get(username="newuser")
    assert user.project_memberships.exists()

    dashboard = client.get("/")
    assert dashboard.status_code == 200
