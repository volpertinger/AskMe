from django.db import models
from django.contrib.auth.models import User


class Reputation(models.Model):
    value = models.IntegerField

    def __str__(self):
        return str(self.value)


class Profile(User):
    profile_image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.username)


class Question(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField(max_length=8192)
    reputation = models.ForeignKey(Reputation, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    # objects = QuestionManager

    def getHighReputation(self, number):
        return self.objects.all().order_by("reputation")[:number]

    def __str__(self):
        return self.title


class Answer(models.Model):
    text = models.TextField(max_length=8192)
    reputation = models.ForeignKey(Reputation, on_delete=models.CASCADE)
    isCorrect = models.BooleanField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.author)


class Tag(models.Model):
    tag = models.CharField(max_length=32)
    questions = models.ManyToManyField(Question, blank=True)

    def __str__(self):
        return self.tag
