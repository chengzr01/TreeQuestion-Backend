from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=20, null=False)
    password = models.CharField(max_length=20, null=True)
    role = models.CharField(max_length=20, default="student")
