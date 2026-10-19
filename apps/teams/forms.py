
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Membership

User = get_user_model()


class AddMemberForm(forms.Form):
    username = forms.CharField(max_length=150)
    role = forms.ChoiceField(
        choices=[
            (Membership.Role.ADMIN, "Admin"),
            (Membership.Role.MEMBER, "Member"),
        ]
    )

    def __init__(self, *args, project, **kwargs):
        super().__init__(*args, **kwargs)
        self.project = project

    def clean_username(self):
        username = self.cleaned_data["username"]

        user = User.objects.filter(username=username).first()
        if user is None:
            raise ValidationError("User does not exist.")

        if Membership.objects.filter(
            project=self.project,
            user=user,
        ).exists():
            raise ValidationError("User is already a project member.")

        return username
