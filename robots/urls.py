from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('cat/', views.categories),
]
