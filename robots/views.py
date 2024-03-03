from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse('Страница о роботах.')


def categories(request, cat_id):
    return HttpResponse(f'<h1>Статьи по категориям.</h1><p>cat_id: {cat_id}</p>')


def archive(request, year):
    if year > 2024:  # можно использовать time, получив значение текущего года
        raise Http404()
    return HttpResponse(f'<h1>Архив по годам.</h1><p>{year}</p>')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена.</h1>')