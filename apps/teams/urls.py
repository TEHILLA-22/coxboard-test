from django.urls import path
from .views import add_member, remove_member

urlpatterns = [
    path(
        "projects/<uuid:project_id>/add/",
        add_member,
        name="member-add",
    ),
    path(
        "projects/<uuid:project_id>/<uuid:membership_id>/remove/",
        remove_member,
        name="member-remove",
    ),
]