from __future__ import annotations

from django.db import transaction
from django.db.models import Max

from apps.boards.models import Column, Project
from apps.core.models import AuditEvent
from apps.tasks.models import Comment, Task


def _next_sequence(project: Project) -> int:
    value = (
        Task.objects.filter(project=project)
        .aggregate(max_seq=Max("sequence"))
        .get("max_seq")
        or 0
    )
    return value + 1

def _record_event(
    *,
    project: Project,
    task: Task | None,
    actor,
    action: str,
    field_name: str = "",
    before: str = "",
    after: str = "",
    message: str = "",
) -> None:
    AuditEvent.objects.create(
        project=project,
        task=task,
        actor=actor,
        action=action,
        field_name=field_name,
        before=before,
        after=after,
        message=message,
    )

@transaction.atomic
def create_task(
    *,
    project: Project,
    reporter,
    title: str,
    description: str = "",
    column: Column | None = None,
    assignee=None,
    priority: str = Task.Priority.MEDIUM,
    due_date=None,
    labels=None,
) -> Task:
    board = project.board
    target_column = column or board.columns.order_by("position").first()
    sequence = _next_sequence(project)
    task = Task.objects.create(
        project=project,
        board=board,
        column=target_column,
        sequence=sequence,
        key=f"{project.key_prefix}-{sequence}",
        title=title,
        description=description,
        assignee=assignee,
        reporter=reporter,
        priority=priority,
        due_date=due_date,
        order=sequence,
    )
    if labels:
        task.labels.set(labels)
    _record_event(
        project=project,
        task=task,
        actor=reporter,
        action="create",
        message=f"Created task {task.key}",
    )
    return task

@transaction.atomic
def update_task(*, task: Task, actor, **changes) -> Task:
    tracked = ["title", "description", "priority", "assignee", "due_date", "column"]
    for field in tracked:
        if field in changes and changes[field] is not None:
            old = getattr(task, field)
            new = changes[field]
            if old != new:
                setattr(task, field, new)
                _record_event(
                    project=task.project,
                    task=task,
                    actor=actor,
                    action="update",
                    field_name=field,
                    before=str(old),
                    after=str(new),
                    message=f"Updated {field}",
                )
    task.save()
    if "labels" in changes and changes["labels"] is not None:
        before = ", ".join(task.labels.values_list("name", flat=True))
        task.labels.set(changes["labels"])
        after = ", ".join(task.labels.values_list("name", flat=True))
        if before != after:
            _record_event(
                project=task.project,
                task=task,
                actor=actor,
                action="label_change",
                field_name="labels",
                before=before,
                after=after,
                message="Updated labels",
            )
    return task

@transaction.atomic
def move_task(*, task: Task, actor, column: Column) -> Task:
    old_column = task.column
    task.column = column
    task.order = (
        Task.objects.filter(column=column)
        .aggregate(max_order=Max("order"))
        .get("max_order")
        or 0
    ) + 1
    task.save(update_fields=["column", "order", "updated_at"])
    _record_event(
        project=task.project,
        task=task,
        actor=actor,
        action="move",
        field_name="column",
        before=old_column.name,
        after=column.name,
        message=f"Moved to {column.name}",
    )
    return task

@transaction.atomic
def add_comment(*, task: Task, author, body: str) -> Comment:
    comment = Comment.objects.create(task=task, author=author, body=body)
    _record_event(
        project=task.project,
        task=task,
        actor=author,
        action="comment",
        message="Added comment",
    )
    return comment
