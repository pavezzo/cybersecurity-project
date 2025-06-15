from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    SECURITY_QUESTIONS = [
        "What year were you born?",
        "What color was you first car?",
        "What is your favorite food?",
    ]

    security_question = models.TextField()
    security_answer = models.TextField()


class Picture(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    name = models.TextField(unique=True)
    description = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
