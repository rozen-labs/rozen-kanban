from __future__ import annotations

from django import forms

from apps.tasks.models import Comment, Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "priority", "assignee", "due_date", "labels"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 6}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "labels": forms.SelectMultiple(attrs={"size": 6}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {"body": forms.Textarea(attrs={"rows": 4, "placeholder": "Write a comment..."})}
