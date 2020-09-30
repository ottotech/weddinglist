# Django imports
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

# Project imports
from gifts.listing.service import Lister
from gifts.storage.django_orm import PSQLStorage

from rest_framework.views import APIView

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


class UserWeddingListApiView(APIView):

    def get(self, request, service=lister):

        user_wedding_list = service.get_user_wedding_list(request.user.id)

        user_id = user_wedding_list.user.user_id

        gifts = [
            {"gift_id": g.gift_id,
             "name": g.name,
             "brand_name": g.brand.name,
             "price": g.price,
             "active": g.active,
             "stock": g.stock,
             "status": g.stock}
            for g in user_wedding_list.list
        ]

        return JsonResponse({"user_id": user_id, "gifts": gifts}, status=200)



