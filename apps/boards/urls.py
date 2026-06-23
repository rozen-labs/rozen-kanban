from django.urls import path

from apps.boards import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("projects/new/", views.project_create, name="project_create"),
    path("projects/<slug:slug>/", views.board_view, name="board"),
    path("projects/<slug:slug>/labels/new/", views.project_label_create, name="label_create"),
]
