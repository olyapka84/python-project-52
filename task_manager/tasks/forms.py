from django import forms
from django.contrib.auth import get_user_model

from task_manager.users.utils import format_user_display

from .models import Task

User = get_user_model()


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", 
                                                 "rows": 4}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "executor": forms.Select(attrs={"class": "form-select"}),
            "labels": forms.SelectMultiple(attrs={"class": "form-select", 
                                                  "size": 5}),
        }
        labels = {
            "name": "Имя",
            "description": "Описание",
            "status": "Статус",
            "executor": "Исполнитель",
            "labels": "Метки",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["executor"].queryset = User.objects.all().order_by("id")
        self.fields["executor"].label_from_instance = format_user_display
