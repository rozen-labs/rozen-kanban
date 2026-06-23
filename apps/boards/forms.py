from __future__ import annotations

from django import forms

from apps.boards.models import Label, Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description"]
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}

class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ["name", "color"]
