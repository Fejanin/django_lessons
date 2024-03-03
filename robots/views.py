from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.urls import reverse


# Create your views here.

def index(request):
    return HttpResponse('Страница о роботах.')


def categories(request, cat_id):
    return HttpResponse(f'<h1>Статьи по категориям.</h1><p>cat_id: {cat_id}</p>')


def archive(request, year):
    if year == 1950:
        uri = reverse('cat_id', args=(1, ))
        return redirect(uri)
    if year > 2024:  # можно использовать time, получив значение текущего года
        raise Http404()
    if year < 2000:
        return redirect('home')  # временное перемещение (302); ('/', permanent=True) ==> постоянное (301)
    return HttpResponse(f'<h1>Архив по годам.</h1><p>{year}</p>')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена.</h1>')