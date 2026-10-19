
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from apps.projects.permissions import (
    get_accessible_project,
    require_project_permission,
)
from .forms import AddMemberForm
from .models import Membership

User = get_user_model()


@login_required
def add_member(request, project_id):
    project = get_accessible_project(request.user, project_id)
    require_project_permission(
        request.user, project, "manage_members"
    )

    if request.method == "POST":
        form = AddMemberForm(request.POST, project=project)

        if form.is_valid():
            user = User.objects.get(
                username=form.cleaned_data["username"]
            )

            try:
                with transaction.atomic():
                    Membership.objects.create(
                        project=project,
                        user=user,
                        role=form.cleaned_data["role"],
                    )
            except IntegrityError:
                form.add_error(
                    "username", "User is already a member."
                )
            else:
                return redirect("project-detail", pk=project.pk)
    else:
        form = AddMemberForm(project=project)

    return render(
        request,
        "shared/form.html",
        {"form": form, "title": "Add Team Member"},
    )


@login_required
def remove_member(request, project_id, membership_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    project = get_accessible_project(request.user, project_id)
    actor = require_project_permission(
        request.user, project, "manage_members"
    )

    with transaction.atomic():
        target = get_object_or_404(
            Membership.objects.select_for_update(),
            pk=membership_id,
            project=project,
        )

        if target.role == Membership.Role.OWNER:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("Cannot remove project owner.")

        if (
            actor.role == Membership.Role.ADMIN
            and target.role == Membership.Role.ADMIN
        ):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("Admins cannot remove admins.")

        target.delete()

    return redirect("project-detail", pk=project.pk)
