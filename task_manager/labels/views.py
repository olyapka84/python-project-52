from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import LabelForm
from .models import Label


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = "labels/index.html"
    context_object_name = "labels"


class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/form.html"
    success_url = reverse_lazy("labels:index")

    def form_valid(self, form):
        messages.success(self.request, _("Метка успешно создана"))
        return super().form_valid(form)


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/form.html"
    success_url = reverse_lazy("labels:index")

    def form_valid(self, form):
        messages.success(self.request, _("Метка успешно обновлена"))
        return super().form_valid(form)


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = "labels/confirm_delete.html"
    success_url = reverse_lazy("labels:index")

    def dispatch(self, request, *args, **kwargs):
        label = self.get_object()
        if label.labeled_tasks.exists():
            messages.error(request, _("Нельзя удалить метку, так как она связана с задачей"))
            return self.get_redirect_url()
        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self):
        from django.shortcuts import redirect
        return redirect("labels:index")

    def delete(self, request, *args, **kwargs):
        messages.success(request, _("Метка успешно удалена"))
        return super().delete(request, *args, **kwargs)
