from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import LogoutView, LoginView
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm, CustomAuthenticationForm


class UserListView(ListView):
    model = User
    template_name = "users/index.html"
    context_object_name = "users"
    ordering = ["username"]


class OnlySelfMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_authenticated and obj.pk == self.request.user.pk

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.error(self.request, "У вас нет прав для изменения другого пользователя.")
        return redirect("users:list")


class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Пользователь успешно зарегистрирован")
        return response


class UserUpdateView(OnlySelfMixin, UpdateView):
    model = User
    fields = ["username", "first_name", "last_name"]
    template_name = "users/update.html"
    success_url = reverse_lazy("users:list")

    def get_object(self, queryset=None):
        return self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для изменения другого пользователя.")
        return redirect("users:list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Изменения успешно сохранены.")
        return response


class UserDeleteView(LoginRequiredMixin, OnlySelfMixin, DeleteView):
    model = User
    template_name = "users/confirm_delete.html"
    success_url = reverse_lazy("users:list")
    login_url = "users:login"

    def handle_no_permission(self):
        messages.error(self.request, "Вы не авторизованы! Пожалуйста, выполните вход.")
        return super().handle_no_permission()

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if user.created_tasks.exists() or user.executed_tasks.exists():
            messages.error(request, "Нельзя удалить пользователя, связанного с задачами.")
            return redirect("users:list")
        return super().dispatch(request, *args, **kwargs)


class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = CustomAuthenticationForm
    next_page = reverse_lazy("home")

    def form_valid(self, form):
        messages.success(self.request, "Вы залогинены")
        return super().form_valid(form)


class UserLogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "Вы разлогинены")
        return redirect("home")

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "Вы разлогинены")
        return redirect("home")
