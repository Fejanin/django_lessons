from django.contrib import admin, messages
from .models import Robot, Category


@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_create', 'is_published', 'cat', 'brief_info')
    list_display_links = ('title', )
    ordering = ['-time_create', 'title']
    list_editable = ('is_published', 'cat',)
    list_per_page = 3
    actions = ['set_published', 'set_draft']

    @admin.display(description='Краткое описание', ordering='content')
    def brief_info(self, robot: Robot):
        return f'Описание {len(robot.content)} символов.'

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

