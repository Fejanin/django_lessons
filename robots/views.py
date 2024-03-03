from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse('Страница о роботах.')


def categories(request, cat_id):
    return HttpResponse(f'<h1>Статьи по категориям.</h1><p>cat_id: {cat_id}</p>')


def archive(request, year):
    return HttpResponse(f'<h1>Архив по годам.</h1><p>{year}</p>')
