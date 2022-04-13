from django.core.management.base import BaseCommand
from baseApplication.models import Profile, Reputation, Question, Answer, Tag


def clearDB():
    Tag.objects.all().delete()
    Answer.objects.all().delete()
    Question.objects.all().delete()
    Reputation.objects.all().delete()


def addTag(number):
    tag = Tag(tag="Tag#" + str(number)).save()


def addAnswer(number):
    text = "This is some text for answer #" + str(number)
    Answer(text=text).save()


def addReputation(number):
    reputation_value = 100 * number
    reputation = Reputation(value=reputation_value).save()


def addAllTables(number):
    addTag(number)
    addReputation(number)
    # addAnswer(number)


class Command(BaseCommand):
    help = 'The Zen of Python'

    def handle(self, *args, **options):
        clearDB()
        number = 10

        for i in range(number):
            addAllTables(number)
