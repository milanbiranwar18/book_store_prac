from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    mobile_num = models.IntegerField(max_length=100)
    location = models.CharField(max_length=100)
