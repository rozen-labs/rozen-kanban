from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.boards.models import Column, Label
from apps.tasks.models import Comment, Task

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "author", "author_username", "body", "created_at"]
        read_only_fields = ["author", "created_at"]

class TaskSerializer(serializers.ModelSerializer):
    assignee_username = serializers.CharField(source="assignee.username", read_only=True)
    reporter_username = serializers.CharField(source="reporter.username", read_only=True)
    labels = serializers.PrimaryKeyRelatedField(queryset=Label.objects.all(), many=True, required=False)

    class Meta:
        model = Task
        fields = [
            "id", "project", "board", "column", "sequence", "key", "title", "description",
            "priority", "assignee", "assignee_username", "reporter", "reporter_username",
            "due_date", "order", "labels", "created_at", "updated_at",
        ]
        read_only_fields = ["project", "board", "sequence", "key", "reporter", "order", "created_at", "updated_at"]

class TaskCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, allow_blank=True)
    priority = serializers.ChoiceField(choices=Task.Priority.choices, default=Task.Priority.MEDIUM)
    column = serializers.PrimaryKeyRelatedField(queryset=Column.objects.all(), required=False)
    assignee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    due_date = serializers.DateField(required=False, allow_null=True)
    labels = serializers.PrimaryKeyRelatedField(queryset=Label.objects.all(), many=True, required=False)

class MoveTaskSerializer(serializers.Serializer):
    column = serializers.PrimaryKeyRelatedField(queryset=Column.objects.all())

class CommentCreateSerializer(serializers.Serializer):
    body = serializers.CharField()
