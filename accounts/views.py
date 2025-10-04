# accounts/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import LogoutView, LoginView
from django.shortcuts import redirect
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm


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
        messages.error(self.request, "У вас нет прав для изменения другого пользователя.")
        return redirect("users:list")


class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "users/create.html"
    success_url = reverse_lazy("users:list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Пользователь успешно создан.")
        return response


class UserUpdateView(LoginRequiredMixin, OnlySelfMixin, UpdateView):
    model = User
    fields = ["username", "first_name", "last_name"]
    template_name = "users/update.html"
    success_url = reverse_lazy("users:list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Изменения успешно сохранены.")
        return response


class UserDeleteView(LoginRequiredMixin, OnlySelfMixin, DeleteView):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users:list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Пользователь успешно удалён.")
        return super().delete(request, *args, **kwargs)


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    next_page = reverse_lazy('home')  # куда редиректить после входа

    def form_valid(self, form):
        messages.success(self.request, "Вы успешно залогинены.")
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Вы успешно разлогинены.")
        return super().dispatch(request, *args, **kwargs)

