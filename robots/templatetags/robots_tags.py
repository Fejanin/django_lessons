from django import template
import robots.views as views
from robots.models import Category

register = template.Library()


@register.inclusion_tag('robots/list_categories.html')
def show_categories(cat_selected):
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}
