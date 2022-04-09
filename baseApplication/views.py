from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

QUESTIONS = [
    {
        "title": f"Title {i}",
        "text": f"some text for question #{i}",
        "number": f"{i}",
        "reputation": f"{i * 123 + 32}"
    } for i in range(22)
]

ANSWERS = [
    {
        "text": f"some text in answer #{i}",
        "reputation": f"{i * 107 - 54}"
    } for i in range(22)
]


def index(request):
    page = request.GET.get('page')
    paginator = Paginator(QUESTIONS, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, поставим первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимальной, доставить последнюю страницу результатов
        posts = paginator.page(paginator.num_pages)
    return render(request, "index.html", {"questions": QUESTIONS, "isMember": True, "page": page,
                                          "posts": posts})


def addQuestion(request):
    return render(request, "addQuestion.html", {"isMember": True})


def login(request):
    return render(request, "login.html", {"isMember": False})


def registration(request):
    return render(request, "registration.html", {"isMember": False})


def settings(request):
    return render(request, "settings.html", {"isMember": True})


def questionAnswer(request, i: int):
    page = request.GET.get('page')
    paginator = Paginator(ANSWERS, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, поставим первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимальной, доставить последнюю страницу результатов
        posts = paginator.page(paginator.num_pages)
    return render(request, "questionAnswer.html",
                  {"question": QUESTIONS[i], "answers": ANSWERS, "isMember": True, "page": page, "posts": posts})
