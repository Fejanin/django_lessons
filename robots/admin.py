from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Robot, Category


@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
    # fields = ['title', 'content', 'slug', 'cat'] # список полей для создания записей
    # exclude = ['tags', 'is_published'] # список полей, исключенных при создании записи
    readonly_fields = ['post_photo'] # список полей, которые отображаются, но меняются
    prepopulated_fields = {'slug': ('title', )} # заменяет метод save из модели
    filter_horizontal = ['tags']
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'cat')
    list_display_links = ('title', )
    ordering = ['-time_create', 'title']
    list_editable = ('is_published', 'cat',)
    list_per_page = 6
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'cat__name']
    list_filter = ['cat__name', 'is_published']
    save_on_top = True

    @admin.display(description='Фото', ordering='content')
    def post_photo(self, robot: Robot):
        if robot.photo:
            return mark_safe(f'<img src="{robot.photo.url}" width=50>')
        return 'Без фото'

    @admin.action(description='Опубликовать выбранные статьи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Robot.Status.PUBLISHED)
        self.message_user(request, f'Было опубликовано {count} статей.')

    @admin.action(description='Удалить из опубликованных выбранные статьи')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Robot.Status.DRAFT)
        self.message_user(request , f'Было удалено из опубликованных {count} статей.', messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

