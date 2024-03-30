from django.http import HttpResponse
from django.shortcuts import render


def login_user(request):
    return HttpResponse('LOGIN')


def logout_user(request):
    return HttpResponse('LOGOUT')
