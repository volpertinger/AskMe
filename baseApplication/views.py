from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from baseApplication.models import Profile, Like, Dislike, Question, Answer, Tag
from django.http import Http404


def get_posts(request, array):
    page_number = request.GET.get('page')
    paginator = Paginator(array, 5)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Если страница не является целым числом, поставим первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимальной, доставить последнюю страницу результатов
        posts = paginator.page(paginator.num_pages)
    return posts, page_number


def index(request, tag: str = '', sort: str = ''):
    header = "popular questions"
    popular_tags = Tag.manager.get_popular()
    questions = Question.manager.get_popular()
    if sort == "latest":
        header = "latest questions"
        questions = Question.manager.get_latest()
    if tag != '':
        tag = Tag.manager.get_tag_by_title(tag)
        questions = Question.manager.get_by_tag(tag)
        if len(questions) <= 0:
            raise Http404("Tag does not exist")
    posts, page_number = get_posts(request, questions)
    return render(request, "index.html",
                  {"questions": questions, "isMember": True, "tag": tag, "page": page_number,
                   "posts": posts, "tags": popular_tags, "header": header})


def addQuestion(request):
    popular_tags = Tag.manager.get_popular()
    return render(request, "addQuestion.html", {"isMember": True, "tags": popular_tags})


def login(request):
    popular_tags = Tag.manager.get_popular()
    return render(request, "login.html", {"isMember": False, "tags": popular_tags})


def registration(request):
    popular_tags = Tag.manager.get_popular()
    return render(request, "registration.html", {"isMember": False, "tags": popular_tags})


def settings(request):
    popular_tags = Tag.manager.get_popular()
    return render(request, "settings.html", {"isMember": True, "tags": popular_tags})


def questionAnswer(request, id_question: int):
    popular_tags = Tag.manager.get_popular()
    question = Question.manager.all().filter(id=id_question)
    if len(question) <= 0:
        raise Http404("Question does not exist")
    question = question[0]
    answers = Answer.manager.get_popular(question)
    posts, page_number = get_posts(request, answers)
    return render(request, "questionAnswer.html",
                  {"question": question, "answers": answers, "isMember": True, "page": page_number, "posts": posts,
                   "tags": popular_tags})
