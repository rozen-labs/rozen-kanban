from __future__ import annotations

from rest_framework import serializers

from apps.boards.models import Board, Column, Label, Project, ProjectMembership


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ["id", "name", "key", "position", "is_done"]

class BoardSerializer(serializers.ModelSerializer):
    columns = ColumnSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ["id", "project", "wip_limit", "columns"]

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ["id", "name", "color"]

class ProjectMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMembership
        fields = ["id", "user", "role"]

class ProjectSerializer(serializers.ModelSerializer):
    board = BoardSerializer(read_only=True)
    labels = LabelSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ["id", "name", "slug", "key_prefix", "description", "board", "labels"]
        read_only_fields = ["slug", "key_prefix", "board", "labels"]

class ProjectCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=120)
    description = serializers.CharField(required=False, allow_blank=True)
