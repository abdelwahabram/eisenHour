from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    pass


class Task(models.Model):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=900)
    date = models.DateField(default=timezone.now)
    importance = models.BooleanField()
    status = models.BooleanField(default=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="tasks")
    def save(self, *args, **kwargs):
        if self.date < timezone.now().date():
            raise ValidationError("The date cannot be in the past!")
        super(Task, self).save(*args, **kwargs)
