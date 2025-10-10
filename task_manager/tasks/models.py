from django.db import models
from django.contrib.auth.models import User

from task_manager.labels.models import Label
from task_manager.statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, 
                               related_name="tasks")
    author = models.ForeignKey(User, on_delete=models.PROTECT, 
                               related_name="created_tasks")
    executor = models.ForeignKey(User, on_delete=models.PROTECT, null=True, 
                                 blank=True, related_name="executed_tasks")
    created_at = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField(Label, related_name="labeled_tasks", 
                                    blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name
