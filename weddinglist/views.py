# -*- coding: utf-8 -*-
# Django imports
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

# Project imports
from .decorators import redirect_if_guest


@redirect_if_guest
def home(request):
    if not request.user.is_authenticated:
        return redirect(settings.LOGIN_URL)
    return render(request, 'home.html', {'home': True})


@method_decorator(redirect_if_guest, name="dispatch")
class GuestAddingView(TemplateView):
    template_name = "guest_adding.html"


