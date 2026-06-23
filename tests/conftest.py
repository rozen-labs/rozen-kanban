import pytest
from django.contrib.auth import get_user_model

from apps.boards.services import create_project_with_board

User = get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(username="dev", email="dev@example.com", password="password123", role=User.Role.DEVELOPER)

@pytest.fixture
def manager(db):
    return User.objects.create_user(username="manager", email="manager@example.com", password="password123", role=User.Role.MANAGER)

@pytest.fixture
def project(user):
    return create_project_with_board(creator=user, name="Alpha Team", description="Main workspace")
