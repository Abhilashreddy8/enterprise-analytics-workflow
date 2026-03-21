# Create your models here.
from django.db import models
from django.conf import settings



class Task(models.Model):

    STATUS_CHOICES = (
        ('YTS', 'Yet To Start'),
        ('WIP', 'Work In Progress'),
        ('HOLD', 'On Hold'),
        ('COMPLETED', 'Completed'),
    )

    REQUEST_TYPE_CHOICES = (
        ('ABD', 'ABD'),
        ('DSA', 'DSA'),
        ('FDS', 'FDS'),
    )

    # System fields
    task_id = models.AutoField(primary_key=True)
    task_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='YTS')
    task_start_date = models.DateTimeField(auto_now_add=True)

    # Business fields
    project_id = models.CharField(max_length=100, unique=True)
    project_name = models.CharField(max_length=255)
    request_type = models.CharField(max_length=10, choices=REQUEST_TYPE_CHOICES)
    cab_id = models.CharField(max_length=100)

    # Relations
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_tasks'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tasks'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_name

class HoldHistory(models.Model):

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='holds')

    hold_start = models.DateTimeField(auto_now_add=True)
    hold_end = models.DateTimeField(null=True, blank=True)

    reason = models.TextField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.task.project_name} - HOLD"

class AssignmentHistory(models.Model):

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='assignments')

    assigned_from = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_from_history'
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_to_history'
    )

    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assigned_by_history'
    )

    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.project_name} reassigned"