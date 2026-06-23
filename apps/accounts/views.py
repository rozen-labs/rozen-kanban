from __future__ import annotations

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.accounts.forms import LoginForm, RegistrationForm
from apps.boards.services import create_project_with_board


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        create_project_with_board(creator=user, name=f"{user.username}'s Workspace", description="Personal workspace")
        messages.success(request, "Welcome aboard.")
        return redirect("dashboard")
    return render(request, "accounts/register.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(request, username=form.cleaned_data["identifier"], password=form.cleaned_data["password"])
        if user is None:
            form.add_error(None, "Invalid credentials")
        else:
            login(request, user)
            messages.success(request, "Logged in.")
            return redirect("dashboard")
    return render(request, "accounts/login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")
