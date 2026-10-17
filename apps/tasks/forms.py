
from django import forms
from django.core.exceptions import ValidationError

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            "title",
            "description",
            "status",
            "priority",
            "assigned_to",
            "due_date",
        )
        widgets = {
            "due_date": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            )
        }

    def __init__(self, *args, project, **kwargs):
        super().__init__(*args, **kwargs)
        self.project = project
        
        from apps.accounts.models import User
        self.fields["assigned_to"].queryset = User.objects.filter(
            id__in=project.memberships.values("user_id")
        )
        self.fields["due_date"].input_formats = [
            "%Y-%m-%dT%H:%M",
        ]

    def clean_assigned_to(self):
        user = self.cleaned_data.get("assigned_to")
        if user and not self.project.memberships.filter(user=user).exists():
            raise ValidationError("Assignee must belong to this project.")
        return user
