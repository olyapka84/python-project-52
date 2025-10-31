from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from .filters import TaskFilter
from .models import Task
from .forms import TaskForm


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = "tasks/index.html"
    context_object_name = "tasks"
    login_url = "login"
    filterset_class = TaskFilter

    def get_queryset(self):
        return (
            super().get_queryset()
            .select_related("status", "author", "executor")
            .prefetch_related("labels")
            .order_by("id")
        )


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/detail.html"
    context_object_name = "task"
    login_url = "login"


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/form.html"
    success_url = reverse_lazy("tasks:index")
    login_url = "login"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Task created successfully")
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/form.html"
    success_url = reverse_lazy("tasks:index")
    login_url = "login"

    def form_valid(self, form):
        messages.success(self.request, "Task updated successfully")
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = "tasks/confirm_delete.html"
    success_url = reverse_lazy("tasks:index")
    login_url = "login"

    def test_func(self):
        return self.get_object().author_id == self.request.user.id

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, "Only the author can delete the task")
            return redirect("tasks:index")
        return super().handle_no_permission()

    def post(self, request, *args, **kwargs):
        messages.success(self.request, "Task deleted successfully")
        return super().post(request, *args, **kwargs)
