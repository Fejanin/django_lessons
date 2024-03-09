from django import template
import robots.views as views


register = template.Library()


@register.simple_tag()
def get_categories():
    return views.cat_db


@register.inclusion_tag('robots/list_categories.html')
def show_categories(cat_selected):
    cats = views.cat_db
    return {'cats': cats, 'cat_selected': cat_selected}
