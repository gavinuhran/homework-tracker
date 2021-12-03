from django.db import models
# Create your models here.
class Task(models.Model):
    STATUSES = (
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Complete', 'Complete'),
    )

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    project = models.CharField(default="placeholder", max_length=100)
    due_date = models.DateField()
    description = models.CharField(max_length=500)
    status = models.CharField(max_length=50, choices=STATUSES)
    total_time = models.IntegerField()

class TimeEntry(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    task = models.IntegerField() # User enters task id