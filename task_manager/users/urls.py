# users/urls.py
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import (
    UserListView,
    UserUpdateView,
    UserDeleteView,
    UserCreateView,
    UserLogoutView,
    UserLoginView,
)

app_name = "users"

urlpatterns = [
    path("", UserListView.as_view(), name="list"),
    path("create/", UserCreateView.as_view(), name="create"),
    path("<int:pk>/update/", UserUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", UserDeleteView.as_view(), name="delete"),
    path("login/", UserLoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/edit/", UserUpdateView.as_view(), name="profile_edit"),
    path(
        "password/change/",
        auth_views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
            success_url=reverse_lazy("users:password_change_done"),
        ),
        name="password_change",
    ),
    path(
        "password/change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html"
        ),
        name="password_change_done",
    ),
]
