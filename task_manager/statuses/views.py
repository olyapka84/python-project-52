from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .models import Status
from .forms import StatusForm


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses/index.html"
    context_object_name = "statuses"
    login_url = "login"


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/form.html"
    success_url = reverse_lazy("statuses:index")
    login_url = "login"

    def form_valid(self, form):
        messages.success(self.request, "Status created successfully")
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/form.html"
    success_url = reverse_lazy("statuses:index")
    login_url = "login"

    def form_valid(self, form):
        messages.success(self.request, "Status updated successfully")
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = "statuses/confirm_delete.html"
    success_url = reverse_lazy("statuses:index")
    login_url = "login"

    def post(self, request, *args, **kwargs):
        status = self.get_object()
        if status.tasks.exists():
            messages.error(
                request,
                "Cannot delete status because it is in use",
            )
            return redirect("statuses:index")
        response = super().post(request, *args, **kwargs)
        messages.success(request, "Status deleted successfully")
        return response
