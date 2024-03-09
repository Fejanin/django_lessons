from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string


menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'addpage'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Войти', 'url_name': 'login'},
]

data_db = [
    {
        'id': 1,
        'title': 'QUANTEC PA Arctic',
        'content': '<strong>Робот</strong> функционирующий при экстремально низких температурах. \nОн создан для работы преимущественно в морозильных камерах, при температурах до -30 °C.',
        'is_published': True
    },
    {
        'id': 2,
        'title': 'FANUC M-2000iA/1200',
        'content': 'пятиосевой грузоподъемный робот поднимающий до 1200 кг и перемещающий этот груз на расстояние до 3,7 м — идеален в качестве погрузчика, так как работает без участия человека, что практически сводит к нулю опасность травматизма.',
        'is_published': False
    },
    {
        'id': 3,
        'title': 'UR10',
        'content': 'Самый крупный из манипуляторов Universal Robots и это коллаборативный робот, проще говоря — он создан для работы с другим оборудованием и помощи в работе человеку.',
        'is_published': True
    },
]

def index(request):
    data = {
        'title': 'Главная страница о роботах.',
        'menu': menu,
        'posts': data_db,
    }
    return render(request, 'robots/index.html', context=data)


def about(request):
    data = {
        'title': 'О нас',
        'menu': menu,
    }
    return render(request, 'robots/about.html', context=data)


def show_post(request, post_id):
    return HttpResponse(f'Отображение статьи с id: {post_id}.')


def addpage(request):
    return HttpResponse('Добавление статьи.')


def contact(request):
    return HttpResponse('Обратная связь.')


def login(request):
    return HttpResponse('Авторизация.')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена.</h1>')