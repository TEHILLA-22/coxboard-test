from django.urls import path
from .views import (
    ProjectCreateView,
    ProjectDetailView,
    ProjectListView,
    ProjectUpdateView,
)

urlpatterns = [
    path("", ProjectListView.as_view(), name="project-list"),
    path("new/", ProjectCreateView.as_view(), name="project-create"),
    path("<uuid:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path("<uuid:pk>/edit/", ProjectUpdateView.as_view(), name="project-update"),
]