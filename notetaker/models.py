from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    pass

class Team(models.Model):
    team_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_by")
    name = models.CharField(max_length=32, unique=True)
    member = models.ManyToManyField(User, related_name="teams", blank=True)
    image = models.ImageField(upload_to="team/images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'List'),
        ('in_progress', 'Taken'),
        ('done', 'Completed'),
    ]
    task_author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="task_author")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="tasks", null=True, blank=True)
    title = models.CharField(max_length=16, verbose_name="task")
    description = models.TextField(max_length=256, verbose_name="description")
    image = models.ImageField(upload_to="task/images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="task_taken", blank=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="todo", verbose_name="status")
    
    def save(self, *args, **kwargs):
        if self.assigned_to and self.status == 'todo':
            self.status = 'in_progress'
        super().save(*args, **kwargs)

class Invitation(models.Model):
    token = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="invitations")
    created_at = models.DateField(auto_now_add=True)
