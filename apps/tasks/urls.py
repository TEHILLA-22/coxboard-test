from django.urls import path
from .views import create_task, update_task

urlpatterns = [
    path("projects/<uuid:project_id>/new/", create_task, name="task-create"),
    path("<uuid:pk>/edit/", update_task, name="task-update"),
]