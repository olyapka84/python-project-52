from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect

from .forms import LabelForm
from .models import Label


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = "labels/index.html"
    context_object_name = "labels"
    login_url = "users:login"


class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/form.html"
    success_url = reverse_lazy("labels:index")
    login_url = "users:login"

    def form_valid(self, form):
        messages.success(self.request, "Метка успешно создана")
        return super().form_valid(form)


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/form.html"
    success_url = reverse_lazy("labels:index")
    login_url = "users:login"

    def form_valid(self, form):
        messages.success(self.request, "Метка успешно обновлена")
        return super().form_valid(form)


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = "labels/confirm_delete.html"
    success_url = reverse_lazy("labels:index")
    login_url = "users:login"

    def post(self, request, *args, **kwargs):
        label = self.get_object()
        if label.labeled_tasks.exists():
            messages.error(request, "Нельзя удалить метку: есть связанные задачи.")
            return redirect("labels:index")
        response = super().post(request, *args, **kwargs)
        messages.success(request, "Метка удалена.")
        return response