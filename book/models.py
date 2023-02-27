from django.db import models

# Create your models here.
from user.models import User


class Book(models.Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    price = models.IntegerField(default=0.00)
    quantity = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
