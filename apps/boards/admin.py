from django.contrib import admin

from apps.boards.models import Board, Column, Label, Project, ProjectMembership


class ColumnInline(admin.TabularInline):
    model = Column
    extra = 0

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "key_prefix", "created_by", "created_at")
    search_fields = ("name", "slug", "key_prefix")

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("project", "wip_limit")
    inlines = [ColumnInline]

@admin.register(ProjectMembership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("project", "user", "role")
    search_fields = ("project__name", "user__username")

@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ("name", "project", "color")
    search_fields = ("name", "project__name")
