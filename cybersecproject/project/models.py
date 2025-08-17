import uuid

from django.contrib.auth.models import User
from django.db import models


class Picture(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    name = models.TextField(unique=True)
    description = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
