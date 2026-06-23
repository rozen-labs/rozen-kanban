from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class Task(TimeStampedModel):
    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical"

    project = models.ForeignKey("boards.Project", on_delete=models.CASCADE, related_name="tasks")
    board = models.ForeignKey("boards.Board", on_delete=models.CASCADE, related_name="tasks")
    column = models.ForeignKey("boards.Column", on_delete=models.PROTECT, related_name="tasks")
    sequence = models.PositiveIntegerField()
    key = models.CharField(max_length=24, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=16, choices=Priority.choices, default=Priority.MEDIUM)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tasks")
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="reported_tasks")
    due_date = models.DateField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    labels = models.ManyToManyField("boards.Label", blank=True, related_name="tasks")

    class Meta:
        ordering = ["column__position", "order", "sequence"]
        unique_together = [("project", "sequence")]

    def __str__(self) -> str:
        return f"{self.key} {self.title}"

class Comment(TimeStampedModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="task_comments")
    body = models.TextField()

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"Comment by {self.author} on {self.task.key}"
