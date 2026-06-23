from __future__ import annotations

from django.shortcuts import get_object_or_404
from rest_framework import routers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.boards.models import Project
from apps.boards.serializers import ProjectCreateSerializer, ProjectSerializer
from apps.tasks.models import Task
from apps.tasks.serializers import CommentCreateSerializer, CommentSerializer, MoveTaskSerializer, TaskCreateSerializer, TaskSerializer
from apps.tasks.services import add_comment, create_task, move_task, update_task
from kanban.permissions import can_manage_project


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.select_related("board", "created_by").prefetch_related("board__columns", "labels")

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser or getattr(user, "role", None) == "admin":
            return qs
        return qs.filter(memberships__user=user).distinct()

    def create(self, request, *args, **kwargs):
        serializer = ProjectCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        from apps.boards.services import create_project_with_board

        project = create_project_with_board(creator=request.user, **serializer.validated_data)
        return Response(ProjectSerializer(project, context={"request": request}).data, status=201)

class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.select_related("project", "board", "column", "assignee", "reporter").prefetch_related("labels")

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser or getattr(user, "role", None) == "admin":
            return qs
        return qs.filter(project__memberships__user=user).distinct()

    @action(detail=False, methods=["post"], url_path="projects/(?P<project_slug>[^/.]+)/tasks")
    def create_for_project(self, request, project_slug=None):
        project = get_object_or_404(Project, slug=project_slug)
        if not can_manage_project(request.user, project):
            return Response({"detail": "Forbidden"}, status=403)
        serializer = TaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = create_task(
            project=project,
            reporter=request.user,
            title=serializer.validated_data["title"],
            description=serializer.validated_data.get("description", ""),
            column=serializer.validated_data.get("column"),
            assignee=serializer.validated_data.get("assignee"),
            priority=serializer.validated_data.get("priority", Task.Priority.MEDIUM),
            due_date=serializer.validated_data.get("due_date"),
            labels=serializer.validated_data.get("labels"),
        )
        return Response(TaskSerializer(task, context={"request": request}).data, status=201)

    @action(detail=True, methods=["post"])
    def move(self, request, pk=None):
        task = self.get_object()
        serializer = MoveTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = move_task(task=task, actor=request.user, column=serializer.validated_data["column"])
        return Response(TaskSerializer(task, context={"request": request}).data)

    @action(detail=True, methods=["patch"])
    def update_fields(self, request, pk=None):
        task = self.get_object()
        serializer = TaskSerializer(task, data=request.data, partial=True, context={"request": request})
        serializer.is_valid(raise_exception=True)
        labels = serializer.validated_data.pop("labels", None) if "labels" in serializer.validated_data else None
        assignee = serializer.validated_data.pop("assignee", None) if "assignee" in serializer.validated_data else None
        updated = update_task(task=task, actor=request.user, labels=labels, assignee=assignee, **serializer.validated_data)
        if labels is not None:
            updated.labels.set(labels)
        return Response(TaskSerializer(updated, context={"request": request}).data)

    @action(detail=True, methods=["get", "post"], url_path="comments")
    def comments(self, request, pk=None):
        task = self.get_object()
        if request.method == "GET":
            return Response(CommentSerializer(task.comments.select_related("author").all(), many=True).data)
        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = add_comment(task=task, author=request.user, body=serializer.validated_data["body"])
        return Response(CommentSerializer(comment).data, status=201)

router = routers.DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"tasks", TaskViewSet, basename="task")
