from django.db import models

# Create your models here.
class Task(models.Model):
    STATUSES = (
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Complete', 'Complete'),
    )
    title = models.CharField(max_length=200)
    project = models.CharField(default="placeholder", max_length=100)
    due_date = models.DateTimeField()
    description = models.CharField(max_length=500)
    status = models.CharField(max_length=50, choices=STATUSES)
    total_time = models.IntegerField()