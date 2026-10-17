
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from apps.projects.models import Project
from apps.teams.models import Membership
from .forms import TaskForm
from .models import Task


def editable_project(user, project_id):
    return get_object_or_404(
        Project,
        pk=project_id,
        memberships__user=user,
        status=Project.Status.ACTIVE,
    )


@login_required
def create_task(request, project_id):
    project = editable_project(request.user, project_id)

    if request.method == "POST":
        form = TaskForm(request.POST, project=project)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.created_by = request.user
            task.save()
            return redirect("project-detail", pk=project.pk)
    else:
        form = TaskForm(project=project)

    return render(
        request,
        "shared/form.html",
        {"form": form, "title": "Create Task"},
    )


@login_required
def update_task(request, pk):
    task = get_object_or_404(
        Task.objects.select_related("project"),
        pk=pk,
        project__memberships__user=request.user,
        project__status=Project.Status.ACTIVE,
    )

    if request.method == "POST":
        form = TaskForm(
            request.POST,
            instance=task,
            project=task.project,
        )
        if form.is_valid():
            form.save()
            return redirect("project-detail", pk=task.project_id)
    else:
        form = TaskForm(instance=task, project=task.project)

    return render(
        request,
        "shared/form.html",
        {"form": form, "title": "Update Task"},
    )
