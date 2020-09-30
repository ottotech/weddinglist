# Django imports
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

# Project imports
from gifts.listing.service import Lister
from gifts.storage.django_orm import PSQLStorage


# Setup storage
storage = None

if settings.STORAGE_TYPE == "psql":
    storage = PSQLStorage()
else:
    storage = PSQLStorage()

lister = Lister(storage=storage)


@require_http_methods(["GET"])
def show_all_gifts(request, service=lister):

    gifts = service.get_all_gifts_available()

    res = [
        {"gift_id": g.gift_id,
         "name": g.name,
         "brand_name": g.brand.name,
         "price": g.price,
         "active": g.active,
         "stock": g.stock}
        for g in gifts
    ]

    return JsonResponse(
        data={"gifts": res},
        status=200
    )
