from django.db import models
from user.models import User

# Create your models here.


class Tree(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=100)
    description = models.JSONField(null=True)


class Knowledge(models.Model):
    concept = models.CharField(max_length=1000)
    level = models.CharField(max_length=1000)
    field = models.CharField(max_length=1000)
    ideation = models.TextField()
    knowledge = models.TextField()
    datetime = models.DateTimeField()


class Graph(models.Model):
    concept_text = models.CharField(max_length=1000)
    field = models.CharField(max_length=1000)
    knowledge_text = models.TextField()
    graph_text = models.TextField()
    datetime = models.DateTimeField()


class Key(models.Model):
    source = models.CharField(max_length=1000)
    label = models.CharField(max_length=1000)
    target = models.CharField(max_length=1000)
    key = models.TextField()
    datetime = models.DateTimeField()


class Distractor(models.Model):
    source = models.CharField(max_length=1000)
    label = models.CharField(max_length=1000)
    target = models.CharField(max_length=1000)
    template = models.TextField()
    key = models.TextField()
    heuristics = models.TextField()
    distractors = models.TextField()
    datetime = models.DateTimeField()


class Question(models.Model):
    concept = models.CharField(max_length=100)
    field = models.CharField(max_length=100)
    level = models.CharField(max_length=100)
    qtype = models.CharField(max_length=100)
    key_text = models.TextField()
    distractor_text = models.TextField()
    stem = models.TextField()
    options = models.TextField()
    answer = models.TextField()
    datetime = models.DateTimeField()