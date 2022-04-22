from django.contrib import auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse

from baseApplication.models import Profile, Like, Dislike, Question, Answer, Tag
from django.http import Http404
from .forms import LoginForm, RegistrationForm


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
    user = request.user
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
                  {"questions": questions, "tag": tag, "page": page_number,
                   "posts": posts, "tags": popular_tags, "header": header, "user": user})


def addQuestion(request):
    popular_tags = Tag.manager.get_popular()
    user = request.user
    return render(request, "addQuestion.html", {"user": user, "tags": popular_tags})


def logout(request):
    auth.logout(request)
    return redirect('/')


def login(request):
    popular_tags = Tag.manager.get_popular()
    user = request.user

    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            auth.login(request, user)
            if user:
                return redirect('/')
            else:
                form.add_error("password", "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, "login.html", {"tags": popular_tags, "form": form, "user": user})


def registration(request):
    popular_tags = Tag.manager.get_popular()

    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            auth.authenticate(username=username, password=raw_password)
            return redirect('/login/')
    else:
        form = RegistrationForm()
    return render(request, "registration.html", {"tags": popular_tags, "form": form})


def settings(request):
    popular_tags = Tag.manager.get_popular()
    user = request.user

    return render(request, "settings.html", {"user": user, "tags": popular_tags})


def questionAnswer(request, id_question: int):
    popular_tags = Tag.manager.get_popular()
    user = request.user

    question = Question.manager.all().filter(id=id_question)
    if len(question) <= 0:
        raise Http404("Question does not exist")
    question = question[0]
    answers = Answer.manager.get_popular(question)
    posts, page_number = get_posts(request, answers)
    return render(request, "questionAnswer.html",
                  {"question": question, "answers": answers, "page": page_number, "posts": posts,
                   "tags": popular_tags, "user": user})
