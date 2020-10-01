# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.conf import settings


def home(request):
    if not request.user.is_authenticated:
        return redirect(settings.LOGIN_URL)
    return render(request, 'home.html', {'home': True})


