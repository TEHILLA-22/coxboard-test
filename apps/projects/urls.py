from django.urls import path
from .views import (
    ProjectCreateView,
    ProjectDetailView,
    ProjectListView,
    ProjectUpdateView,
    archive_project,
    restore_project,
    delete_project,
)

urlpatterns = [
    path("", ProjectListView.as_view(), name="project-list"),
    path("new/", ProjectCreateView.as_view(), name="project-create"),
    path("<uuid:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path("<uuid:pk>/edit/", ProjectUpdateView.as_view(), name="project-update"),
    
    path("<uuid:pk>/archive/", archive_project, name="project-archive"),
path("<uuid:pk>/restore/", restore_project, name="project-restore"),
path("<uuid:pk>/delete/", delete_project, name="project-delete"),
]