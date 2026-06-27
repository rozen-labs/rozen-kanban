import pytest
from django.urls import reverse

from apps.boards.models import Column
from apps.tasks.services import create_task, move_task


@pytest.mark.django_db
def test_board_column_counts_reflect_visible_tasks(user, project, client):
    client.force_login(user)
    backlog = Column.objects.get(board=project.board, key="backlog")
    review = Column.objects.get(board=project.board, key="review")

    backlog_task = create_task(project=project, reporter=user, title="Backlog work", column=backlog)
    create_task(project=project, reporter=user, title="Review work", column=review)

    response = client.get(reverse("board", kwargs={"slug": project.slug}))
    counts = {column["column"].key: column["count"] for column in response.context["columns"]}

    assert counts == {
        "backlog": 1,
        "todo": 0,
        "in-progress": 0,
        "review": 1,
        "done": 0,
    }

    filtered = client.get(reverse("board", kwargs={"slug": project.slug}), {"q": "Backlog"})
    filtered_counts = {column["column"].key: column["count"] for column in filtered.context["columns"]}
    assert filtered_counts == {
        "backlog": 1,
        "todo": 0,
        "in-progress": 0,
        "review": 0,
        "done": 0,
    }

    moved = move_task(task=backlog_task, actor=user, column=review)
    assert moved.column == review

    refreshed = client.get(reverse("board", kwargs={"slug": project.slug}))
    refreshed_counts = {column["column"].key: column["count"] for column in refreshed.context["columns"]}
    assert refreshed_counts["backlog"] == 0
    assert refreshed_counts["review"] == 2
