# -*- coding: utf-8 -*-

# Django imports
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView

# Project imports
from weddinglist.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('', home, name='home'),
    path('api/', include("gifts.urls"), name='home'),
    path('add-guest/', TemplateView.as_view(template_name="guest_adding.html")),
]
