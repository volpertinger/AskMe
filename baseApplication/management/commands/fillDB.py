from django.core.management.base import BaseCommand
from baseApplication.models import Profile, Reputation, Question, Answer, Tag

USERS_COUNT = 10  # 10 000
QUESTION_COUNT = 10  # 100 000
ANSWERS_COUNT = 10  # 1 000 000
TAGS_COUNT = 10  # 10 000
REPUTATION_COUNT = 10  # 2 000 000


def clearDB():
    Tag.objects.all().delete()
    Answer.objects.all().delete()
    Question.objects.all().delete()
    Reputation.objects.all().delete()
    # чтобы мою админку оно не чистило каждый раз
    Profile.objects.all().exclude(username="killoboker").delete()


def addUser(number):
    username = "User#" + str(number)
    password = "Password" + str(number)
    email = "email" + str(number) + "@mail.ru"
    Profile(username=username, password=password, email=email).save()


def addTag(number):
    Tag(tag="Tag#" + str(number)).save()


def addAnswer(number):
    text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et ' \
           'dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ' \
           'ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu ' \
           'fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt ' \
           'mollit anim id est laborum. '
    question = Question.objects.all()[number % QUESTION_COUNT]
    reputation = Reputation.objects.all()[number % REPUTATION_COUNT]
    author = Profile.objects.all()[number % USERS_COUNT]
    Answer(text=text, question=question, reputation=reputation, author=author).save()


def addQuestion(number):
    title = "Question Title#" + str(number)
    text = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the " \
           "industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and " \
           "scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap " \
           "into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the " \
           "release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing " \
           "software like Aldus PageMaker including versions of Lorem Ipsum. Why do we use it?It is a long " \
           "established fact that a reader will be distracted by the readable content of a page when looking at its " \
           "layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, " \
           "as opposed to using 'Content here, content here', making it look like readable English. Many desktop " \
           "publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search " \
           "for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over " \
           "the years, sometimes by accident, sometimes on purpose (injected humour and the like). #" + str(number)
    reputation = Reputation.objects.all()[number % REPUTATION_COUNT]
    author = Profile.objects.all()[number % USERS_COUNT]
    Question(title=title, text=text, reputation=reputation, author=author).save()


def addReputation(number):
    reputation_value = 100 * number % 100000
    Reputation(value=reputation_value).save()


def addAllTables():
    for i in range(TAGS_COUNT):
        addTag(i)
    for i in range(REPUTATION_COUNT):
        addReputation(i)
    for i in range(USERS_COUNT):
        addUser(i)
    for i in range(QUESTION_COUNT):
        addQuestion(i)
    for i in range(ANSWERS_COUNT):
        addAnswer(i)


class Command(BaseCommand):
    help = 'The Zen of Python'

    def handle(self, *args, **options):
        clearDB()
        addAllTables()
