from __future__ import annotations

from django.db import transaction
from django.utils.text import slugify

from apps.boards.models import Board, Column, Label, Project, ProjectMembership

DEFAULT_COLUMNS = [
    ("Backlog", "backlog", False),
    ("Todo", "todo", False),
    ("In Progress", "in-progress", False),
    ("Review", "review", False),
    ("Done", "done", True),
]

@transaction.atomic
def create_project_with_board(*, creator, name: str, description: str = "") -> Project:
    base_slug = slugify(name)[:120] or "project"
    slug = base_slug
    suffix = 2
    while Project.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{suffix}"
        suffix += 1
    prefix = "".join(ch for ch in slug.upper() if ch.isalnum())[:6] or "KANBAN"
    while Project.objects.filter(key_prefix=prefix).exists():
        prefix = f"{prefix[:5]}X"
    project = Project.objects.create(
        name=name,
        slug=slug,
        key_prefix=prefix,
        description=description,
        created_by=creator,
    )
    board = Board.objects.create(project=project)
    for position, (column_name, key, is_done) in enumerate(DEFAULT_COLUMNS):
        Column.objects.create(board=board, name=column_name, key=key, position=position, is_done=is_done)
    ProjectMembership.objects.create(project=project, user=creator, role=ProjectMembership.Role.MANAGER)
    return project

@transaction.atomic
def create_label(project: Project, name: str, color: str = "#4f46e5") -> Label:
    return Label.objects.create(project=project, name=name, color=color)
