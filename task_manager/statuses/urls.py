from django.urls import path
from .views import (
    StatusListView, StatusCreateView, StatusUpdateView, StatusDeleteView
)

urlpatterns = [
    path("", StatusListView.as_view(), name="statuses_index"),
    path("create/", StatusCreateView.as_view(), name="statuses_create"),
    path("<int:pk>/update/", StatusUpdateView.as_view(), 
         name="statuses_update"),
    path("<int:pk>/delete/", StatusDeleteView.as_view(), 
         name="statuses_delete"),
]
