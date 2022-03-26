from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

QUESTIONS = [
    {
        "title": f"Title {i}",
        "text": f"some text for question #{i}",
        "number": f"{i}",
        "reputation": f"{i * 123 + 32}"
    } for i in range(10)
]

ANSWERS = [
    {
        "text": f"some text in answer #{i}",
        "reputation": f"{i * 107 - 54}"
    } for i in range(10)
]


def index(request):
    return render(request, "index.html", {"questions": QUESTIONS, "isMember": True})


def addQuestion(request):
    return render(request, "addQuestion.html", {"isMember": True})


def login(request):
    return render(request, "login.html", {"isMember": False})


def registration(request):
    return render(request, "registration.html", {"isMember": False})


def questionAnswer(request, i: int):
    return render(request, "questionAnswer.html", {"question": QUESTIONS[i], "answer": ANSWERS[i], "isMember": True})
