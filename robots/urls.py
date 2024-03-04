from django.urls import path, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('cat/<int:cat_id>/', views.categories, name='cat_id'),
    path('archive/<year4:year>', views.archive, name="archive"),
]

