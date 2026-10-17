
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
)

from apps.teams.models import Membership
from .forms import ProjectForm
from .models import Project


def accessible_projects(user):
    return Project.objects.filter(
        Q(owner=user) | Q(memberships__user=user)
    ).distinct()


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "projects/list.html"
    context_object_name = "projects"

    def get_queryset(self):
        return accessible_projects(self.request.user)


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "projects/detail.html"

    def get_queryset(self):
        return accessible_projects(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = self.object.tasks.all()
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "shared/form.html"
    success_url = reverse_lazy("project-list")

    def form_valid(self, form):
        with transaction.atomic():
            project = form.save(commit=False)
            project.owner = self.request.user
            project.save()

            Membership.objects.create(
                project=project,
                user=self.request.user,
                role=Membership.Role.OWNER,
            )

        self.object = project
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(self.get_success_url())


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "shared/form.html"
    success_url = reverse_lazy("project-list")

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)
