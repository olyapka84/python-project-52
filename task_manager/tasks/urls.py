from django.urls import path
from .views import (
    TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView, TaskDetailView
)

urlpatterns = [
    path("", TaskListView.as_view(), name="tasks_index"),
    path("create/", TaskCreateView.as_view(), name="tasks_create"),
    path("<int:pk>/", TaskDetailView.as_view(), name="tasks_detail"),
    path("<int:pk>/update/", TaskUpdateView.as_view(), name="tasks_update"),
    path("<int:pk>/delete/", TaskDeleteView.as_view(), name="tasks_delete"),
]
