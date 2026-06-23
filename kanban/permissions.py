from __future__ import annotations

from apps.boards.models import Project, ProjectMembership


def is_admin(user) -> bool:
    return bool(user and user.is_authenticated and (user.is_superuser or user.role == "admin"))

def project_role(user, project: Project) -> str | None:
    if not user or not user.is_authenticated:
        return None
    if is_admin(user):
        return "admin"
    membership = ProjectMembership.objects.filter(user=user, project=project).first()
    return membership.role if membership else None

def can_view_project(user, project: Project) -> bool:
    return is_admin(user) or ProjectMembership.objects.filter(user=user, project=project).exists()

def can_manage_project(user, project: Project) -> bool:
    if is_admin(user):
        return True
    return ProjectMembership.objects.filter(user=user, project=project, role__in=["manager", "developer"]).exists()

def can_manage_task(user, task) -> bool:
    if is_admin(user):
        return True
    if task.assignee_id == getattr(user, "id", None):
        return True
    return ProjectMembership.objects.filter(user=user, project=task.project).exists()
