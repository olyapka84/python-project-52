# tasks/filters.py
import django_filters as df
from django import forms
from django.contrib.auth import get_user_model
from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label

User = get_user_model()


class TaskFilter(df.FilterSet):
    status = df.ModelChoiceFilter(
        queryset=Status.objects.all().order_by("id"),
        label="Статус",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    executor = df.ModelChoiceFilter(
        queryset=User.objects.all().order_by("id"),
        label="Исполнитель",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    label = df.ModelChoiceFilter(
        field_name="labels",
        queryset=Label.objects.all().order_by("id"),
        label="Метка",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    self_tasks = df.BooleanFilter(
        method="filter_self_tasks",
        label="Только свои задачи",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = Task
        fields = ["status", "executor", "label", "self_tasks"]

    def __init__(self, data=None, queryset=None, request=None, **kwargs):
        super().__init__(data=data, queryset=queryset,
                         request=request, **kwargs)
        self.request = request
        self.filters["executor"].field.label_from_instance = (
            lambda u: (u.get_full_name().strip()
                       if (u.get_full_name() or "").strip() else u.username)
        )

    def filter_self_tasks(self, queryset, name, value):
        return queryset.filter(author=self.request.user) if value else queryset
