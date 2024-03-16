from django import template
from robots.models import Category, TagPost

register = template.Library()


@register.inclusion_tag('robots/list_categories.html')
def show_categories(cat_selected):
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('robots/list_tags.html')
def show_all_tags():
    return {'tags': TagPost.objects.all()}
