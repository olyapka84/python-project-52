from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django import forms
from django.contrib import messages
from django.contrib.auth import logout, password_validation
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
User = get_user_model()


class UserListView(ListView):
    model = User
    template_name = "users/index.html"
    context_object_name = "users"
    ordering = ["username"]


class OnlySelfMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return (self.request.user.is_authenticated and 
                obj.pk == self.request.user.pk)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request,
                           "You are not authorized! Please log in.")
            return super().handle_no_permission()
        messages.error(self.request,
                       "You do not have permission to modify another user.")
        return redirect("users:list")


class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "User registered successfully")
        return response


class UserUpdateView(OnlySelfMixin, UpdateView):
    model = User
    fields = ["username", "first_name", "last_name"]
    template_name = "users/update.html"
    success_url = reverse_lazy("users:list")

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["password1"] = forms.CharField(
            label="Password",
            required=False,
            widget=forms.PasswordInput(attrs={"class": "form-control"}),
            help_text=password_validation.password_validators_help_text_html(),
        )
        form.fields["password2"] = forms.CharField(
            label="Password confirmation",
            required=False,
            widget=forms.PasswordInput(attrs={"class": "form-control"}),
            help_text="Please enter the password again for confirmation.",
        )
        return form

    def form_valid(self, form):
        p1 = form.cleaned_data.get("password1")
        p2 = form.cleaned_data.get("password2")
        if p1 or p2:
            if not p1 or not p2:
                form.add_error("password2",
                               "Please enter the password twice.")
                return self.form_invalid(form)
            if p1 != p2:
                form.add_error("password2", "The entered passwords do not match.")
                return self.form_invalid(form)
            password_validation.validate_password(p1, self.object)
            form.instance.set_password(p1)
        response = super().form_valid(form)
        messages.success(self.request, "User updated successfully")
        return response


class UserDeleteView(OnlySelfMixin, LoginRequiredMixin, DeleteView):
    model = User
    template_name = "users/confirm_delete.html"
    success_url = reverse_lazy("users:list")
    login_url = "login"

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        if (hasattr(user, "created_tasks") and user.created_tasks.exists()) or \
           (hasattr(user, "executed_tasks") and user.executed_tasks.exists()):
            messages.error(request,
                           "Cannot delete user because they are in use")
            return redirect("users:list")
        messages.success(request, "User deleted successfully")
        return super().post(request, *args, **kwargs)


class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = CustomAuthenticationForm
    next_page = reverse_lazy("home")

    def form_valid(self, form):
        messages.success(self.request, "You are logged in")
        return super().form_valid(form)


class UserLogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You are logged out")
        return redirect("home")

    def get(self, request, *args, **kwargs):
        return redirect("home")
