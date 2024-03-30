from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from .forms import AddPostForm, UploadFileForm
from .models import Robot, Category, TagPost, UploadFiles
from .utils import DataMixin


class RodotHome(DataMixin, ListView):  # миксины добавляются первыми
    template_name = 'robots/index.html'
    context_object_name = 'posts'  # по умолчанию доступ к списку в шаблоне (html) можно получить по object_list
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        return Robot.published.all().select_related('cat')  # оптимизация SQL запросов


@login_required  # можно передать в качестве аргумента адрес переадресации для неавторизованных пользователей (login_url='/path_redirect/')
def about(request):
    contact_list = Robot.published.all()
    paginator = Paginator(contact_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'robots/about.html', {
        'title': 'О сайте',
        'page_obj': page_obj,
    })


class ShowPost(DataMixin, DetailView):  # миксины добавляются первыми
    template_name = 'robots/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Robot.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'robots/addpage.html'
    title_page = 'Добавление статьи'
    # login_url = '/admin/'  # можно указать альтернативный адрес переадрисации, для неавторизованных пользователей

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdatePage(DataMixin, UpdateView):
    model = Robot
    fields = '__all__'  # если нужно отображать не все поля ==> используй список
    template_name = 'robots/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'


def contact(request):
    return HttpResponse('Обратная связь.')


def login(request):
    return HttpResponse('Авторизация.')


class RobotCategory(DataMixin, ListView):
    template_name = 'robots/index.html'
    context_object_name = 'posts'
    allow_empty = False  # если в get_context_data ==> cat получаем пустой список, то сгенерируется ошибка 404

    def get_queryset(self):
        return Robot.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')  # оптимизация SQL запросов

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(
            context,
            title='Категория - ' + cat.name,
            cat_selected=cat.pk,
        )


class TagPostList(DataMixin, ListView):
    template_name = 'robots/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(
            context,
            title='Тег: ' + tag.tag
        )

    def get_queryset(self):
        return Robot.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена.</h1>')