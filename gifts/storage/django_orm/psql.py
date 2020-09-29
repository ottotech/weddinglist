# Python imports
from typing import List

# Django imports
from django.contrib.auth.models import User

# Project imports
from gifts.models import Gift
from gifts import listing
from gifts.models import GiftList


class PSQLStorage(object):

    @staticmethod
    def get_all_gifts_available() -> List[listing.Gift]:
        objs = Gift.objects.all().order_by("name")

        gift_list = []

        for obj in objs:
            gift = listing.Gift(
                name=obj.name,
                brand=listing.Brand(name=obj.brand.name),
                price=obj.price,
                active=obj.active,
                stock=obj.in_stock_qty
            )
            gift_list.append(gift)

        return gift_list

    @staticmethod
    def get_user_wedding_list(user_id: int) -> listing.UserWeddingList:
        user_obj = User.objects.get(id=user_id)
        user = listing.User(
            user_id=user_obj.id,
            name=user_obj.name,
            last_name=user_obj.last_name,
            email=user_obj.email
        )

        qs = GiftList.objects.filter(user_id=user_id)

        user_gifts = []

        for obj in qs:
            user_gift = listing.UserGift(
                name=obj.gift.name,
                brand=obj.gift.brand,
                price=obj.gift.price,
                active=obj.gift.price,
                status=obj.status
            )
            user_gifts.append(user_gift)

        wedding_list = listing.UserWeddingList(user=user, user_gifts=user_gifts)

        return wedding_list



