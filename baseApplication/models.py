import datetime

from django.db import models
from django.contrib.auth.models import User


class QuestionQuerySet(models.QuerySet):
    def popular(self):
        return self.order_by("-reputation__value")

    def latest(self):
        return self.order_by("publish_date")


class QuestionManager(models.Manager):
    def get_queryset(self):
        return QuestionQuerySet(self.model)

    def get_popular(self):
        return self.get_queryset().popular()

    def get_latest(self):
        return self.get_queryset().latest()

    def get_by_tag_title(self, tag_title=None):
        if tag_title is None:
            return self.get_queryset().latest()
        return self.get_queryset().filter(tag__tag=tag_title)


class QuestionPopularManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by("-reputation__value")


class AnswerQuerySet(models.QuerySet):
    def popular(self):
        return self.order_by("reputation__value")

    def latest(self):
        return self.order_by("publish_date")


class AnswerManager(models.Manager):
    def get_queryset(self, question_search=None):
        if question_search is None:
            return QuestionQuerySet(self.model, using=self.db)
        return QuestionQuerySet(self.model, using=self.db).filter(question__id=question_search.id)

    def get_popular(self, question_search=None):
        return self.get_queryset(question_search).popular()

    def get_latest(self, question_search=None):
        return self.get_queryset(question_search).latest()


class TagQuerySet(models.QuerySet):
    def popular(self):
        return self.annotate(num_questions=models.Count("questions")).order_by("num_questions")


class TagManager(models.Manager):
    def get_queryset(self):
        return TagQuerySet(self.model, using=self.db)

    def get_popular(self):
        return self.get_queryset().popular()

    def get_questions(self, question):
        return self.get_queryset().filter(questions=question)


# Models

class Profile(User):
    profile_image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.username)


class Reputation(models.Model):
    value = models.IntegerField()
    authors = models.ManyToManyField(Profile, blank=True)

    def __str__(self):
        return str(self.value)


class Question(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField(max_length=8192)
    reputation = models.ForeignKey(Reputation, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    publish_date = models.DateField(default=datetime.date.today)

    manager = QuestionManager()

    def get_tags(self):
        return Tag.manager.get_questions(self)

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(max_length=8192)
    reputation = models.ForeignKey(Reputation, on_delete=models.CASCADE)
    isCorrect = models.BooleanField(default=False)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    publish_date = models.DateField(default=datetime.date.today)

    manager = AnswerManager()

    def __str__(self):
        return str(self.author) + "/" + str(self.question.title)


class Tag(models.Model):
    tag = models.CharField(max_length=32)
    questions = models.ManyToManyField(Question, blank=True)
    last_update = models.DateField(auto_now=True)

    manager = TagManager()

    def __str__(self):
        return self.tag
