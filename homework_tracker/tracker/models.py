from django.db import models
import uuid
# Create your models here.
class Task(models.Model):
    STATUSES = (
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Complete', 'Complete'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    project = models.CharField(default="placeholder", max_length=100)
    due_date = models.DateField()
    description = models.CharField(max_length=500)
    status = models.CharField(max_length=50, choices=STATUSES)
    total_time = models.IntegerField()