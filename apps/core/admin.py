from django.contrib import admin

from apps.core.models import AuditEvent


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = ("created_at", "project", "task", "actor", "action", "field_name")
    search_fields = ("project__name", "task__key", "message")
