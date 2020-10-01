# Python imports
from typing import List

# Django imports
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import F

# Project imports
from gifts.models import Gift
from gifts.models import Inventory
from gifts import listing
from gifts import adding
from gifts.models import GiftList


class PSQLStorage(object):

    @staticmethod
    def get_all_gifts_available() -> List[listing.Gift]:
        objs = Gift.objects.all().order_by("name")

        gift_list = []

        for obj in objs:
            gift = listing.Gift(
                gift_id=obj.id,
                name=obj.name,
                brand=listing.Brand(name=obj.brand.name),
                price=obj.price,
                active=obj.active,
                stock=obj.in_stock_qty if hasattr(obj, "inventory") else 0
            )
            gift_list.append(gift)

        return gift_list

    @staticmethod
    def get_user_wedding_list(user_id: int) -> listing.UserWeddingList:
        user_obj = User.objects.get(id=user_id)

        user = listing.User(
            user_id=user_obj.id,
            name=user_obj.first_name,
            last_name=user_obj.last_name,
            email=user_obj.email
        )

        qs = GiftList.objects.filter(user_id=user_id)
        user_gifts = []

        for obj in qs:
            user_gift = listing.UserGift(
                gift_id=obj.gift.id,
                name=obj.gift.name,
                brand=obj.gift.brand,
                price=obj.gift.price,
                active=obj.gift.price,
                status=obj.get_status_display()
            )
            user_gifts.append(user_gift)

        wedding_list = listing.UserWeddingList(user=user, user_gifts=user_gifts)

        return wedding_list

    @staticmethod
    def add_gift_to_user_wedding_list(user_id: int, gift_id: int):

        if GiftList.objects.filter(user_id=user_id, gift_id=gift_id).exists():
            raise adding.DuplicatedErr("gift already exists in weeding list.")

        GiftList.objects.create(
            user_id=user_id,
            gift_id=gift_id
        )

        inventory = Inventory.objects.get(gift_id=gift_id)
        inventory.quantity = F("quantity") - 1
        inventory.save()

        now = timezone.now()
        event = adding.GiftAddedEvent(timestamp=now)

        return event



