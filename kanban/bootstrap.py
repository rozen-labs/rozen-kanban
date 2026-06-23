from __future__ import annotations

from django.contrib.auth import get_user_model

from apps.boards.services import create_project_with_board

User = get_user_model()

def bootstrap_admin(*, username: str, email: str, password: str) -> tuple[User, bool]:
    user, created = User.objects.get_or_create(username=username, defaults={"email": email, "role": User.Role.ADMIN})
    changed = False
    if user.email != email:
        user.email = email
        changed = True
    if not user.is_superuser:
        user.is_superuser = True
        changed = True
    if user.role != User.Role.ADMIN:
        user.role = User.Role.ADMIN
        changed = True
    if created or changed:
        user.set_password(password)
        user.save()
    return user, created

def bootstrap_default_workspace(user: User) -> None:
    if not user.project_memberships.exists() and not user.created_projects.exists():
        create_project_with_board(creator=user, name="Engineering", description="Default workspace")
