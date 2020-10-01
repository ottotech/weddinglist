# -*- coding: utf-8 -*-

# Django imports
from django.urls import path

# Project imports
from gifts.views import show_all_gifts
from gifts.views import UserWeddingListApiView
from gifts.views import add_guest


urlpatterns = [
    path('v1/gifts', show_all_gifts),
    path('v1/wedding-list', UserWeddingListApiView.as_view()),
    path('v1/guests', add_guest),
]
