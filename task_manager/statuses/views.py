from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import ProtectedError

from .models import Status
from .forms import StatusForm

class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses/index.html"
    context_object_name = "statuses"
    login_url = "users:login"

class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/form.html"
    success_url = reverse_lazy("statuses_index")
    login_url = "users:login"

    def form_valid(self, form):
        messages.success(self.request, "Статус создан.")
        return super().form_valid(form)

class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/form.html"
    success_url = reverse_lazy("statuses_index")
    login_url = "users:login"

    def form_valid(self, form):
        messages.success(self.request, "Статус обновлён.")
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = "statuses/confirm_delete.html"
    success_url = reverse_lazy("statuses_index")
    login_url = "users:login"

    def post(self, request, *args, **kwargs):
        try:
            messages.success(self.request, "Статус удалён.")
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(self.request, "Нельзя удалить статус: есть связанные задачи.")
            return self.get(request, *args, **kwargs)
