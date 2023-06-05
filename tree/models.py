from django.db import models
from user.models import User

# Create your models here.


class Tree(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=100)
    description = models.JSONField(null=True)


class AnswerSheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    sheet = models.JSONField(null=True)
