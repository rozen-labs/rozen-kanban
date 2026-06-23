from __future__ import annotations

from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class AuditEvent(TimeStampedModel):
    project = models.ForeignKey("boards.Project", on_delete=models.CASCADE, related_name="audit_events")
    task = models.ForeignKey("tasks.Task", on_delete=models.CASCADE, related_name="audit_events", null=True, blank=True)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=64)
    field_name = models.CharField(max_length=64, blank=True)
    before = models.TextField(blank=True)
    after = models.TextField(blank=True)
    message = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.action}: {self.message[:40]}"
