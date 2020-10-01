# Django imports
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponseServerError
from django.views.decorators.http import require_http_methods
from django.db import transaction

# Project imports
from gifts.listing.service import Lister
from gifts.adding.service import Adder
from gifts.deleting.service import Deleter
from gifts.deleting import GiftDeletedFromListEvent
from gifts.deleting import GiftCouldNotBeDeletedErr
from gifts.adding import GiftAddedEvent
from gifts.adding import GiftCouldNotBeAddedEvent
from gifts.adding import DuplicatedErr
from gifts.storage.django_orm import PSQLStorage

# Third party imports
from rest_framework.views import APIView

# Setup storage
storage = None

if settings.STORAGE_TYPE == "psql":
    storage = PSQLStorage()
else:
    storage = PSQLStorage()

# Let's instantiate our services
lister = Lister(storage=storage)
adder = Adder(storage=storage)
deleter = Deleter(storage=storage)


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
    http_method_names = ["get", "post", "delete"]

    def get(self, request, service=lister):

        user_wedding_list = service.get_user_wedding_list(request.user.id)

        user_id = user_wedding_list.user.user_id

        gifts = [
            {"gift_id": g.gift_id,
             "name": g.name,
             "brand_name": g.brand.name,
             "price": g.price,
             "active": g.active,
             "status": g.status}
            for g in user_wedding_list.list
        ]

        return JsonResponse({"user_id": user_id, "gifts": gifts}, status=200)

    @transaction.atomic
    def post(self, request, service=adder):
        try:
            with transaction.atomic():

                gift_id = request.data["gift_id"]

                user_id = request.data["user_id"]

                event = service.add_gift_to_user_wedding_list(
                    user_id=user_id, gift_id=gift_id)

                if event != GiftAddedEvent:
                    if event == GiftCouldNotBeAddedEvent:
                        return JsonResponse({"message": "Product is out of stock."}, status=400)
                    return JsonResponse({}, status=500)

                return JsonResponse({}, status=200)

        except DuplicatedErr as e:
            return JsonResponse({"message": str(e)}, status=400)

        except Exception as e:
            return JsonResponse({}, status=500)

    @transaction.atomic
    def delete(self, request, service=deleter):
        try:
            with transaction.atomic():

                gift_id = request.data["gift_id"]

                user_id = request.data["user_id"]

                event = service.remove_gift_from_user_wedding_list(
                    user_id=user_id, gift_id=gift_id)

                if event != GiftDeletedFromListEvent:
                    return JsonResponse({}, status=500)

                return JsonResponse({}, status=200)

        except GiftCouldNotBeDeletedErr as e:
            return JsonResponse({"message": str(e)}, status=400)

        except Exception as e:
            print(e)
            return JsonResponse({}, status=500)
