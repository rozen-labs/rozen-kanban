from django.contrib import admin

from apps.tasks.models import Comment, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("key", "title", "project", "column", "priority", "assignee", "due_date")
    search_fields = ("key", "title", "description")
    list_filter = ("priority", "column__name", "project__name")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("task", "author", "created_at")
