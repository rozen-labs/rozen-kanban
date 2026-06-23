from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from apps.boards.models import Column, Project
from apps.tasks.forms import CommentForm, TaskForm
from apps.tasks.models import Task
from apps.tasks.services import add_comment, create_task, move_task, update_task
from kanban.permissions import can_manage_project, can_view_project


@login_required
def task_create(request, slug: str):
    project = get_object_or_404(Project, slug=slug)
    if not can_manage_project(request.user, project):
        raise Http404()
    form = TaskForm(request.POST or None)
    form.fields["labels"].queryset = project.labels.all()
    form.fields["assignee"].queryset = request.user.__class__.objects.filter(project_memberships__project=project).distinct()
    if request.method == "POST" and form.is_valid():
        task = create_task(project=project, reporter=request.user, **form.cleaned_data)
        messages.success(request, f"Task {task.key} created.")
        return redirect("task_detail", key=task.key)
    return render(request, "tasks/task_form.html", {"form": form, "project": project, "title": "Create task"})

@login_required
def task_detail(request, key: str):
    task = get_object_or_404(Task.objects.select_related("project", "board", "column", "assignee", "reporter").prefetch_related("labels", "comments__author", "audit_events__actor"), key=key)
    if not can_view_project(request.user, task.project):
        raise Http404()
    comment_form = CommentForm(request.POST or None)
    if request.method == "POST" and comment_form.is_valid():
        add_comment(task=task, author=request.user, body=comment_form.cleaned_data["body"])
        messages.success(request, "Comment added.")
        return redirect("task_detail", key=key)
    return render(request, "tasks/task_detail.html", {"task": task, "comment_form": comment_form, "can_manage": can_manage_project(request.user, task.project)})

@login_required
def task_edit(request, key: str):
    task = get_object_or_404(Task, key=key)
    if not can_manage_project(request.user, task.project):
        raise Http404()
    form = TaskForm(request.POST or None, instance=task)
    form.fields["labels"].queryset = task.project.labels.all()
    form.fields["assignee"].queryset = request.user.__class__.objects.filter(project_memberships__project=task.project).distinct()
    if request.method == "POST" and form.is_valid():
        updated = update_task(task=task, actor=request.user, **form.cleaned_data)
        updated.labels.set(form.cleaned_data.get("labels", []))
        messages.success(request, "Task updated.")
        return redirect("task_detail", key=task.key)
    return render(request, "tasks/task_form.html", {"form": form, "project": task.project, "task": task, "title": f"Edit {task.key}"})

@login_required
def move_task_view(request, key: str):
    task = get_object_or_404(Task.objects.select_related("project", "column"), key=key)
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)
    if not can_manage_project(request.user, task.project):
        return JsonResponse({"detail": "Forbidden"}, status=403)
    column_id = request.POST.get("column_id") or request.POST.get("column")
    column = get_object_or_404(Column, pk=column_id, board=task.board)
    task = move_task(task=task, actor=request.user, column=column)
    return JsonResponse({"ok": True, "task": task.key, "column": column.name})
