# accounts/views.py
from django.contrib.auth.models import User
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm

class UserListView(ListView):
    model = User
    template_name = "users/index.html"
    context_object_name = "users"
    ordering = ["username"]


class UserUpdateView(UpdateView):
    model = User
    fields = ["username", "first_name", "last_name"]
    template_name = "users/update.html"
    success_url = reverse_lazy("users:list")


class UserDeleteView(DeleteView):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users:list")


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "users/create.html"
    success_url = reverse_lazy("users:list")