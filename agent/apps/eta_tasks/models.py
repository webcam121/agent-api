from django.db import models


class ETATask(models.Model):
    task_name = models.CharField(max_length=255, blank=False, null=False)
    task_kwargs = models.TextField(null=True)
    run_at = models.DateTimeField(null=True, blank=True)
    finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
