from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, related_name='boards', on_delete=models.CASCADE)
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
