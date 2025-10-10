from django.urls import path
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
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/edit/", UserUpdateView.as_view(), name="profile_edit"),
]
