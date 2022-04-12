from django.db import models
from django.contrib import auth


class Reputation(models.Model):
    value = models.IntegerField


class Question(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField(max_length=8192)
    reputation = models.ForeignKey(Reputation, models.CASCADE)
    # author'


class Answer(models.Model):
    text = models.TextField(max_length=8192)
    reputation = models.ForeignKey(Reputation, on_delete=models.CASCADE)
    isCorrect = models.BooleanField()


class Tag(models.Model):
    tag = models.CharField(max_length=32)
    questions = models.ManyToManyField(Question)

# class profile
