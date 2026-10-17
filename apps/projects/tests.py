
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.projects.models import Project
from apps.teams.models import Membership


User = get_user_model()


class ProjectTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(
            username="alice",
            password="TestPassword123!",
        )
        self.bob = User.objects.create_user(
            username="bob",
            password="TestPassword123!",
        )

    def test_project_creation_creates_owner_membership(self):
        self.client.force_login(self.alice)

        response = self.client.post(
            reverse("project-create"),
            {"name": "Coxmos Test", "description": "Deployment test"},
        )

        self.assertEqual(response.status_code, 302)

        project = Project.objects.get(name="Coxmos Test")
        self.assertEqual(project.owner, self.alice)

        self.assertTrue(
            Membership.objects.filter(
                project=project,
                user=self.alice,
                role=Membership.Role.OWNER,
            ).exists()
        )

    def test_other_user_cannot_access_private_project(self):
        project = Project.objects.create(
            name="Private Project",
            owner=self.alice,
        )

        self.client.force_login(self.bob)

        response = self.client.get(
            reverse("project-detail", kwargs={"pk": project.pk})
        )

        self.assertEqual(response.status_code, 404)

    def test_anonymous_user_cannot_create_project(self):
        response = self.client.get(reverse("project-create"))
        self.assertEqual(response.status_code, 302)
