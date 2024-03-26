from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, ListView

from .forms import AddPostForm, UploadFileForm
from .models import Robot, Category, TagPost, UploadFiles

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'addpage'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Войти', 'url_name': 'login'},
]

# def index(request):
#     posts = Robot.published.all().select_related('cat')  # оптимизация SQL запросов
#     data = {
#         'title': 'Главная страница о роботах.',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,
#     }
#     return render(request, 'robots/index.html', context=data)


class RodotHome(ListView):
    # model = Robot  # отбражает все записи, если нужно использовать не все используй get_queryset
    template_name = 'robots/index.html'
    context_object_name = 'posts'  # по умолчанию доступ к списку в шаблоне (html) можно получить по object_list
    extra_context = {
        'title': 'Главная страница о роботах.',
        'menu': menu,
        'cat_selected': 0,
    }

    def get_queryset(self):
        return Robot.published.all().select_related('cat')  # оптимизация SQL запросов

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Главная страница о роботах.'
    #     context['menu'] = menu
    #     context['posts'] = Robot.published.all().select_related('cat')  # оптимизация SQL запросов
    #     context['cat_selected'] = int(self.request.GET.get('cat_id', 0))
    #     return context


        # def handle_uploaded_file(f):
#     with open(f'upload/{f.name}', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # handle_uploaded_file(form.cleaned_data['file'])
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    data = {
        'title': 'О нас',
        'menu': menu,
        'form': form,
    }
    return render(request, 'robots/about.html', context=data)


def show_post(request, post_slug):
    post = get_object_or_404(Robot, slug=post_slug)
    data = {
        'title': 'Главная страница о роботах.',
        'menu': menu,
        'post': post,
        'cat_selected': Robot.objects.get(slug=request.path.split('/')[-2]).cat_id,
    }
    return render(request, 'robots/post.html', context=data)


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # try:
#             #     Robot.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except:
#             #     form.add_error(None, 'Ошибка добавления поста')
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#
#     data = {
#         'menu': menu,
#         'title': 'Добавление статьи',
#         'form': form,
#     }
#     return render(request, 'robots/addpage.html', context=data)


class AddPage(View):
    def get(self, request):
        form = AddPostForm()
        data = {
            'menu': menu,
            'title': 'Добавление статьи',
            'form': form,
        }
        return render(request, 'robots/addpage.html', context=data)

    def post(self, request):
        form = AddPostForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        data = {
            'menu': menu,
            'title': 'Добавление статьи',
            'form': form,
        }
        return render(request, 'robots/addpage.html', context=data)


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

class RobotCategory(ListView):
    template_name = 'robots/index.html'
    context_object_name = 'posts'
    allow_empty = False  # если в get_context_data ==> cat получаем пустой список, то сгенерируется ошибка 404

    def get_queryset(self):
        return Robot.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')  # оптимизация SQL запросов

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['title'] = 'Категория - ' + cat.name
        context['menu'] = menu
        context['cat_selected'] = cat.pk
        return context


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