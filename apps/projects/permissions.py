
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from apps.projects.models import Project
from apps.teams.models import Membership


def get_membership(user, project):
    if not user.is_authenticated:
        raise PermissionDenied("Authentication required.")

    membership = Membership.objects.filter(
        project=project,
        user=user,
    ).first()

    if membership is None:
        raise PermissionDenied("You do not belong to this project.")

    return membership


def get_accessible_project(user, project_id):
    return get_object_or_404(
        Project.objects.filter(
            memberships__user=user
        ),
        pk=project_id,
    )


def require_project_permission(user, project, action):
    membership = get_membership(user, project)
    role = membership.role

    if action == "view":
        return membership

    if action in {"create_task", "edit_task"}:
        if project.status != Project.Status.ACTIVE:
            raise PermissionDenied("Project is archived.")
        return membership

    if action in {
        "delete_task",
        "manage_members",
        "edit_project",
    }:
        if project.status != Project.Status.ACTIVE:
            raise PermissionDenied("Project is archived.")

        if role not in {
            Membership.Role.OWNER,
            Membership.Role.ADMIN,
        }:
            raise PermissionDenied("Insufficient permissions.")

        return membership

    if action in {"archive", "restore", "delete_project"}:
        if role != Membership.Role.OWNER:
            raise PermissionDenied("Owner permission required.")
        return membership

    raise ValueError(f"Unknown permission action: {action}")
