# Python imports
import logging

# Django imports
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.contrib.auth.decorators import login_required

# Project imports
from gifts.listing.service import Lister
from gifts.adding.service import Adder
from gifts.deleting.service import Deleter
from gifts.deleting import GiftDeletedFromListEvent
from gifts.deleting import GiftCouldNotBeDeletedErr
from gifts.adding import GiftAddedEvent
from gifts.adding import GuestAddedEvent
from gifts.adding import GiftCouldNotBeAddedEvent
from gifts.adding import DuplicatedErr
from gifts.adding import GuestDuplicatedErr
from gifts.adding import GuestUsernameDuplicatedErr
from gifts.purchasing import Purchaser
from gifts.purchasing import GiftPurchasedEvent
from gifts.storage.django_orm import PSQLStorage

# Third party imports
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BasicAuthentication

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
purchaser = Purchaser(storage=storage)


logger = logging.getLogger("gifts")


@login_required
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
    http_method_names = ["get", "post", "delete", "put"]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get(self, request, service=lister):

        user_id = request.GET.get("user_id")

        user_wedding_list = service.get_user_wedding_list(user_id)

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

                logger.info(f"user ({user_id}) added gift {gift_id}")
                return JsonResponse({}, status=200)

        except DuplicatedErr as e:
            return JsonResponse({"message": str(e)}, status=400)

        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({}, status=500)

    @transaction.atomic
    def delete(self, request, service=deleter):
        try:
            with transaction.atomic():

                gift_id = request.data["gift_id"]

                user_id = request.data["user_id"]

                event = service.remove_gift_from_user_wedding_list(
                    user_id=user_id, gift_id=gift_id)

                return JsonResponse({}, status=200)

        except GiftCouldNotBeDeletedErr as e:
            return JsonResponse({"message": str(e)}, status=400)

        except Exception as e:
            print(e)
            return JsonResponse({}, status=500)

    def put(self, request, service=purchaser):
        gift_id = request.POST.get("gift_id", "")
        user_id = request.POST.get("user_id", "")

        if gift_id == "" or user_id == "":
            return JsonResponse({"message": "missing fields"}, status=400)

        event = service.purchase_gift(
            guest_id=request.user.id, gift_id=gift_id, user_id_of_wedding_list=user_id)

        return JsonResponse({}, status=200)


@login_required
@require_http_methods(["POST"])
@transaction.atomic
def add_guest(request, service=adder):
    first_name = request.POST.get("first_name", "").strip()
    last_name = request.POST.get("last_name", "").strip()
    username = request.POST.get("username", "").strip()
    password = request.POST.get("password", "").strip()
    user_id = request.POST.get("user_id", "").strip()

    # validation here for simplicity
    if any([
        x == ""
        for x in [first_name, last_name, username, password, user_id]
    ]):
        return JsonResponse({"message": "missing fields"}, status=400)

    try:
        with transaction.atomic():
            event = service.add_guest(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=password
            )
            logger.info(event.message)
            return JsonResponse({}, status=200)

    except GuestDuplicatedErr as e:
        return JsonResponse({"message": str(e)}, status=400)

    except GuestUsernameDuplicatedErr as e:
        return JsonResponse({"message": str(e)}, status=400)

    except Exception as e:
        print(e)
        return JsonResponse({}, status=500)
