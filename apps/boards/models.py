from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils.text import slugify

from apps.core.models import TimeStampedModel


class Project(TimeStampedModel):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    key_prefix = models.CharField(max_length=12, unique=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="created_projects")

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:140]
        if not self.key_prefix:
            prefix = "".join(ch for ch in slugify(self.name).upper() if ch.isalnum())[:6]
            self.key_prefix = prefix or "KANBAN"
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

class Board(TimeStampedModel):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name="board")
    wip_limit = models.PositiveIntegerField(default=0, help_text="0 disables WIP limits")

    def __str__(self) -> str:
        return f"Board: {self.project.name}"

class Column(TimeStampedModel):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="columns")
    name = models.CharField(max_length=80)
    key = models.SlugField(max_length=80)
    position = models.PositiveIntegerField(default=0)
    is_done = models.BooleanField(default=False)

    class Meta:
        ordering = ["position", "id"]
        unique_together = [("board", "key")]

    def __str__(self) -> str:
        return self.name

class ProjectMembership(TimeStampedModel):
    class Role(models.TextChoices):
        MANAGER = "manager", "Manager"
        DEVELOPER = "developer", "Developer"
        VIEWER = "viewer", "Viewer"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="project_memberships")
    role = models.CharField(max_length=16, choices=Role.choices, default=Role.DEVELOPER)

    class Meta:
        unique_together = [("project", "user")]
        ordering = ["project__name", "user__username"]

    def __str__(self) -> str:
        return f"{self.user} @ {self.project} ({self.role})"

class Label(TimeStampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="labels")
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=16, default="#4f46e5")

    class Meta:
        unique_together = [("project", "name")]
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
