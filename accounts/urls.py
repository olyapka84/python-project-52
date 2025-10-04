# accounts/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView
from .views import UserListView, UserUpdateView, UserDeleteView, UserCreateView, UserLogoutView, UserLoginView

app_name = "users"

urlpatterns = [
    path("", UserListView.as_view(), name="list"),
    path("create/", UserCreateView.as_view(), name="create"),
    path("<int:pk>/update/", UserUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", UserDeleteView.as_view(), name="delete"),
    # auth
    path("login/", UserLoginView.as_view(template_name="users/login.html"), name="login"),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
