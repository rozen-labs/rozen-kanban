from django.urls import path

from apps.tasks import views

urlpatterns = [
    path("<str:key>/", views.task_detail, name="task_detail"),
    path("<str:key>/edit/", views.task_edit, name="task_edit"),
    path("<str:key>/move/", views.move_task_view, name="task_move"),
    path("projects/<slug:slug>/tasks/new/", views.task_create, name="task_create"),
]
