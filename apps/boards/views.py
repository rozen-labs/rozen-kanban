from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from apps.boards.forms import LabelForm, ProjectForm
from apps.boards.models import Project
from apps.boards.services import create_label, create_project_with_board
from apps.tasks.forms import TaskForm
from kanban.permissions import can_manage_project, can_view_project


def _visible_projects(user):
    if user.is_superuser or getattr(user, "role", None) == "admin":
        return Project.objects.select_related("board", "created_by").prefetch_related("board__columns", "labels")
    return Project.objects.filter(memberships__user=user).distinct().select_related("board", "created_by").prefetch_related("board__columns", "labels")

@login_required
def dashboard(request):
    projects = _visible_projects(request.user)
    return render(request, "boards/dashboard.html", {"projects": projects, "project_form": ProjectForm()})

@login_required
def project_create(request):
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        project = create_project_with_board(creator=request.user, **form.cleaned_data)
        messages.success(request, f"Project {project.name} created.")
        return redirect("board", slug=project.slug)
    return render(request, "boards/project_form.html", {"form": form, "title": "Create project"})

@login_required
def board_view(request, slug: str):
    project = get_object_or_404(Project.objects.select_related("board").prefetch_related("board__columns", "labels", "tasks__labels", "tasks__assignee", "tasks__reporter", "tasks__column"), slug=slug)
    if not can_view_project(request.user, project):
        raise Http404()
    tasks = project.tasks.select_related("assignee", "reporter", "column").prefetch_related("labels")
    q = request.GET.get("q", "").strip()
    priority = request.GET.get("priority", "").strip()
    assignee = request.GET.get("assignee", "").strip()
    label = request.GET.get("label", "").strip()
    if q:
        tasks = tasks.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(key__icontains=q))
    if priority:
        tasks = tasks.filter(priority=priority)
    if assignee:
        tasks = tasks.filter(assignee__username__icontains=assignee)
    if label:
        tasks = tasks.filter(labels__name__icontains=label)
    tasks = list(tasks.distinct().order_by("column__position", "order", "sequence"))
    columns = project.board.columns.all()
    columns_data = []
    tasks_by_column = {column.id: [] for column in columns}
    column_counts = {column.id: 0 for column in columns}
    for task in tasks:
        tasks_by_column[task.column_id].append(task)
        column_counts[task.column_id] += 1
    for column in columns:
        columns_data.append({
            "column": column,
            "count": column_counts[column.id],
            "tasks": tasks_by_column[column.id],
        })
    task_form = TaskForm()
    task_form.fields["labels"].queryset = project.labels.all()
    task_form.fields["assignee"].queryset = request.user.__class__.objects.filter(project_memberships__project=project).distinct()
    label_form = LabelForm()
    return render(request, "boards/board.html", {
        "project": project,
        "columns": columns_data,
        "task_form": task_form,
        "label_form": label_form,
        "filters": {"q": q, "priority": priority, "assignee": assignee, "label": label},
        "can_manage": can_manage_project(request.user, project),
    })

@login_required
def project_label_create(request, slug: str):
    project = get_object_or_404(Project, slug=slug)
    if not can_manage_project(request.user, project):
        raise Http404()
    form = LabelForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        label = create_label(project, **form.cleaned_data)
        messages.success(request, f"Label {label.name} created.")
        return redirect("board", slug=slug)
    return render(request, "boards/label_form.html", {"form": form, "project": project, "title": "Create label"})
