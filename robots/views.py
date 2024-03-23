from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from .models import Robot, Category, TagPost

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'addpage'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Войти', 'url_name': 'login'},
]

def index(request):
    posts = Robot.published.all().select_related('cat')  # оптимизация SQL запросов
    data = {
        'title': 'Главная страница о роботах.',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'robots/index.html', context=data)


def about(request):
    data = {
        'title': 'О нас',
        'menu': menu,
    }
    return render(request, 'robots/about.html', context=data)


def show_post(request, post_slug):
    post = get_object_or_404(Robot, slug=post_slug)
    data = {
        'title': 'Главная страница о роботах.',
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }
    return render(request, 'robots/post.html', context=data)


def addpage(request):
    return render(request, 'robots/addpage.html', context={'menu': menu, 'title': 'Добавление статьи'})


def contact(request):
    return HttpResponse('Обратная связь.')


def login(request):
    return HttpResponse('Авторизация.')


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Robot.published.filter(cat_id=category.pk).select_related('cat')  # оптимизация SQL запросов
    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'robots/index.html', context=data)

def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Robot.Status.PUBLISHED).select_related('cat')  # оптимизация SQL запросов
    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }
    return render(request, 'robots/index.html', context=data)

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена.</h1>')