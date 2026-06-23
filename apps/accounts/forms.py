from __future__ import annotations

from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.accounts.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "role", "password1", "password2"]

class LoginForm(forms.Form):
    identifier = forms.CharField(label="Username or email")
    password = forms.CharField(widget=forms.PasswordInput)
