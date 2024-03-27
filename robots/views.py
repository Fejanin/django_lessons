from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

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


# def show_post(request, post_slug):
#     post = get_object_or_404(Robot, slug=post_slug)
#     data = {
#         'title': 'Главная страница о роботах.',
#         'menu': menu,
#         'post': post,
#         'cat_selected': Robot.objects.get(slug=request.path.split('/')[-2]).cat_id,
#     }
#     return render(request, 'robots/post.html', context=data)


class ShowPost(DetailView):
    # model = Robot
    template_name = 'robots/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        context['menu'] = menu
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Robot.published, slug=self.kwargs[self.slug_url_kwarg])


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


class AddPage(CreateView):
    form_class = AddPostForm
    # model = Robot  # с классом CreateView
    # fields = '__all__'  # если нужно отображать не все поля ==> используй список # с классом CreateView
    template_name = 'robots/addpage.html'
    # success_url = reverse_lazy('home')   # по умолчанию найдет маршрут по ф-ции get_absolute_url ==> произойдет переход на созданную статью
    extra_context = {
        'menu': menu,
        'title': 'Добавление статьи',
    }


class UpdatePage(UpdateView):
    model = Robot
    fields = '__all__'  # если нужно отображать не все поля ==> используй список
    template_name = 'robots/addpage.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'menu': menu,
        'title': 'Редактирование статьи',
    }


# class AddPage(View):
#     def get(self, request):
#         form = AddPostForm()
#         data = {
#             'menu': menu,
#             'title': 'Добавление статьи',
#             'form': form,
#         }
#         return render(request, 'robots/addpage.html', context=data)
#
#     def post(self, request):
#         form = AddPostForm(request.POST , request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         data = {
#             'menu': menu,
#             'title': 'Добавление статьи',
#             'form': form,
#         }
#         return render(request, 'robots/addpage.html', context=data)


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


# def show_tag_postlist(request, tag_slug):
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#     posts = tag.tags.filter(is_published=Robot.Status.PUBLISHED).select_related('cat')  # оптимизация SQL запросов
#     data = {
#         'title': f'Тег: {tag.tag}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': None,
#     }
#     return render(request, 'robots/index.html', context=data)


class TagPostList(ListView):
    template_name = 'robots/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        context['title'] = 'Тег: ' + tag.tag
        context['menu'] = menu
        context['cat_selected'] = None
        return context

    def get_queryset(self):
        return Robot.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена.</h1>')