# Django imports
from django.contrib import admin

# Project imports
from gifts.models import Brand
from gifts.models import Gift
from gifts.models import Inventory
from gifts.models import GiftList

admin.site.register(Brand)
admin.site.register(Gift)
admin.site.register(Inventory)
admin.site.register(GiftList)

