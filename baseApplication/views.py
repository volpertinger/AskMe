from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from baseApplication.models import Profile, Reputation, Question, Answer, Tag


def index(request, tag: str = ''):
    questions = Question.manager.get_popular()
    page_number = request.GET.get('page')
    paginator = Paginator(questions, 5)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Если страница не является целым числом, поставим первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимальной, доставить последнюю страницу результатов
        posts = paginator.page(paginator.num_pages)
    return render(request, "questionsTag.html",
                  {"questions": questions, "isMember": True, "tag": tag, "page": page_number,
                   "posts": posts})


def addQuestion(request):
    return render(request, "addQuestion.html", {"isMember": True})


def login(request):
    return render(request, "login.html", {"isMember": False})


def registration(request):
    return render(request, "registration.html", {"isMember": False})


def settings(request):
    return render(request, "settings.html", {"isMember": True})


def questionAnswer(request, id_question: int):
    question = Question.manager.all().filter(id=id_question)
    if len(question) <= 0:
        return
        # обработка 404
    question = question[0]
    answers = Answer.manager.get_popular(question)
    page_number = request.GET.get('page')
    paginator = Paginator(answers, 5)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Если страница не является целым числом, поставим первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимальной, доставить последнюю страницу результатов
        posts = paginator.page(paginator.num_pages)
    return render(request, "questionAnswer.html",
                  {"question": question, "answers": answers, "isMember": True, "page": page_number, "posts": posts})
