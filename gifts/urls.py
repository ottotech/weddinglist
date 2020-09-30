# -*- coding: utf-8 -*-

# Django imports
from django.urls import path

# Project imports
from gifts.views import show_all_gifts

urlpatterns = [
    path('v1/gifts', show_all_gifts),
]
