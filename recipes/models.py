from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True)
    title = models.CharField(max_length=255)
    ingredients = models.CharField(max_length=255)
    tools = models.CharField(max_length=255)
    description = models.TextField()
    private = models.BooleanField()

    def __str__(self):
        return f'{self.title} for {self.user.username}'