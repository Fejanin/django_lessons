from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string


menu = ['О сайте', 'Добавить статью', 'Обратная связь', 'Войти']

data_db = [
    {'id': 1, 'title': 'QUANTEC PA Arctic', 'content': 'Робот функционирующий при экстремально низких температурах. Он создан для работы преимущественно в морозильных камерах, при температурах до -30 °C.', 'is_published': True},
    {'id': 2, 'title': 'FANUC M-2000iA/1200', 'content': 'пятиосевой грузоподъемный робот поднимающий до 1200 кг и перемещающий этот груз на расстояние до 3,7 м — идеален в качестве погрузчика, так как работает без участия человека, что практически сводит к нулю опасность травматизма.', 'is_published': False},
    {'id': 3, 'title': 'UR10', 'content': 'Самый крупный из манипуляторов Universal Robots и это коллаборативный робот, проще говоря — он создан для работы с другим оборудованием и помощи в работе человеку.', 'is_published': True},
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