from django.db import models
from django.contrib.auth.models import User


class Reputation(models.Model):
    value = models.IntegerField


class Profile(User):
    profile_image = models.ImageField(null=True, blank=True)


class Question(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField(max_length=8192)
    reputation = models.ForeignKey(Reputation, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Answer(models.Model):
    text = models.TextField(max_length=8192)
    reputation = models.ForeignKey(Reputation, on_delete=models.CASCADE)
    isCorrect = models.BooleanField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Tag(models.Model):
    tag = models.CharField(max_length=32)
    questions = models.ManyToManyField(Question, blank=True)
