import django_filters as df
from django import forms
from django.contrib.auth import get_user_model

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.utils import format_user_display

from .models import Task

User = get_user_model()


class TaskFilter(df.FilterSet):
    status = df.ModelChoiceFilter(
        queryset=Status.objects.all().order_by("id"),
        label="Status",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    executor = df.ModelChoiceFilter(
        queryset=User.objects.all().order_by("id"),
        label="Executor",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    label = df.ModelChoiceFilter(
        field_name="labels",
        queryset=Label.objects.all().order_by("id"),
        label="Label",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    self_tasks = df.BooleanFilter(
        method="filter_self_tasks",
        label="Only my tasks",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = Task
        fields = ["status", "executor", "label", "self_tasks"]

    def __init__(self, data=None, queryset=None, request=None, **kwargs):
        super().__init__(data=data, queryset=queryset,
                         request=request, **kwargs)
        self.request = request
        self.filters["executor"].field.label_from_instance = format_user_display

    def filter_self_tasks(self, queryset, name, value):
        return queryset.filter(author=self.request.user) if value else queryset
