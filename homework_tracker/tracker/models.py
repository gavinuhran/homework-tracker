from django.db import models

# Create your models here.
class Task(models.Model):
    STATUSES = (
        ('N', 'Not Started'),
        ('I', 'In Progress'),
        ('C', 'Complete'),
    )
    title = models.CharField(max_length=200)
    due_date = models.DateTimeField()
    description = models.TextField()
    status = models.CharField(max_length=1, choices=STATUSES)
    total_time = models.IntegerField()