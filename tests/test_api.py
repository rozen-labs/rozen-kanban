import pytest
from rest_framework.test import APIClient

from apps.boards.models import Column
from apps.boards.services import create_label
from apps.tasks.models import Task


@pytest.mark.django_db
def test_api_project_task_comment_and_move(user, project):
    client = APIClient()
    client.force_authenticate(user=user)

    project_payload = {"name": "Beta Team", "description": "API created workspace"}
    response = client.post("/api/projects/", project_payload, format="json")
    assert response.status_code == 201
    api_project_slug = response.data["slug"]

    label = create_label(project, "backend", "#2563eb")
    task_payload = {
        "title": "Ship API",
        "description": "Use the API",
        "priority": Task.Priority.HIGH,
        "labels": [label.pk],
    }
    create_resp = client.post(
        f"/api/tasks/projects/{project.slug}/tasks/",
        task_payload,
        format="json",
    )
    assert create_resp.status_code == 201
    task_id = create_resp.data["id"]

    column = Column.objects.get(board=project.board, key="review")
    move_resp = client.post(f"/api/tasks/{task_id}/move/", {"column": column.pk}, format="json")
    assert move_resp.status_code == 200
    assert move_resp.data["column"] == column.pk

    comment_resp = client.post(
        f"/api/tasks/{task_id}/comments/",
        {"body": "Looks good"},
        format="json",
    )
    assert comment_resp.status_code == 201
    assert comment_resp.data["body"] == "Looks good"

    list_resp = client.get("/api/tasks/")
    assert list_resp.status_code == 200
    assert any(item["id"] == task_id for item in list_resp.data)
    assert api_project_slug
