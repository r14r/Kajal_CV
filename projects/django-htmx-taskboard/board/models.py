from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=120)
    note = models.TextField(max_length=500, blank=True)
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["done", "-created_at", "-id"]

    def __str__(self):
        return self.title
