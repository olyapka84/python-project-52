from django.http import Http404
from django.shortcuts import render
from django.conf import settings


def index(request):
    return render(request, "index.html")


def rollbar_test(request):
    if not settings.DEBUG:
        raise Http404("Not found")
    raise RuntimeError("Rollbar test: искусственная ошибка для проверки")