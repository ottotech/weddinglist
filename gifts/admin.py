# Django imports
from django.contrib import admin

# Project imports
from gifts.models import Brand
from gifts.models import Gift
from gifts.models import Inventory

admin.site.site_header = "THE WEDDING LIST ADMIN SITE"

admin.site.register(Brand)
admin.site.register(Gift)
admin.site.register(Inventory)

