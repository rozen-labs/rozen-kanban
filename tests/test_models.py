import pytest

from apps.boards.models import Column, ProjectMembership
from apps.boards.services import create_label
from apps.core.models import AuditEvent
from apps.tasks.models import Comment
from apps.tasks.services import add_comment, create_task, move_task, update_task


@pytest.mark.django_db
def test_project_bootstrap_creates_board_and_columns(project):
    assert project.board.columns.count() == 5
    assert project.memberships.filter(role=ProjectMembership.Role.MANAGER).exists()

@pytest.mark.django_db
def test_task_lifecycle_records_audit(user, project):
    label = create_label(project, "bug", "#ef4444")
    task = create_task(project=project, reporter=user, title="Fix it", labels=[label])
    assert task.key.startswith(project.key_prefix)
    assert task.labels.count() == 1
    next_column = Column.objects.get(board=project.board, key="in-progress")
    moved = move_task(task=task, actor=user, column=next_column)
    assert moved.column == next_column
    update_task(task=moved, actor=user, title="Fix it now")
    comment = add_comment(task=moved, author=user, body="Working on it")
    assert isinstance(comment, Comment)
    assert AuditEvent.objects.filter(task=moved).count() >= 3
