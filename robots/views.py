from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse('Страница о роботах.')


def categories(request):
    return HttpResponse('<h1>Статьи по категориям.</h1>')