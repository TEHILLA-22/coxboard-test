
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render

from apps.tasks.models import Task
from .views import accessible_projects


@login_required
def dashboard(request):
    projects = accessible_projects(request.user)

    tasks = Task.objects.filter(
        project__in=projects
    )

    stats = tasks.aggregate(
        total=Count("id"),
        completed=Count(
            "id",
            filter=Q(status=Task.Status.DONE),
        ),
        in_progress=Count(
            "id",
            filter=Q(status=Task.Status.IN_PROGRESS),
        ),
    )

    return render(
        request,
        "dashboard/index.html",
        {
            "projects": projects[:6],
            "project_count": projects.count(),
            "stats": stats,
            "recent_tasks": tasks.order_by("-created_at")[:8],
        },
    )
