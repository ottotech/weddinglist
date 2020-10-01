# Python imports
from decimal import Decimal
from typing import List

# Project imports
from gifts.listing.brand import Brand
from gifts.listing.user import User


class BaseGift(object):
    __slots__ = [
        "__gift_id",
        "__name",
        "__brand",
        "__price",
        "__active",
    ]

    def __init__(self, gift_id: int, name: str, brand: Brand, price: Decimal, active: bool):
        self.__gift_id = gift_id
        self.__name = name
        self.__brand = brand
        self.__price = price
        self.__active = active

    @property
    def gift_id(self):
        return self.__gift_id

    @property
    def name(self):
        return self.__name

    @property
    def brand(self):
        return self.__brand

    @property
    def price(self):
        return self.__price

    @property
    def active(self):
        return self.__active


class Gift(BaseGift):

    __slots__ = [
        "__stock"
    ]

    def __init__(self, stock: int, *args, **kwargs):
        super(Gift, self).__init__(*args, **kwargs)
        self.__stock = stock

    @property
    def stock(self):
        return self.__stock


class UserGift(BaseGift):

    __slots__ = [
        "__status"
    ]

    def __init__(self, status: str, *args, **kwargs):
        super(UserGift, self).__init__(*args, **kwargs)
        self.__status = status

    @property
    def status(self):
        return self.__status


class UserWeddingList(object):

    __slots__ = [
        "__user",
        "__list",
    ]

    def __init__(self, user: User, user_gifts: List[UserGift]):
        self.__user = user
        self.__list = user_gifts

    @property
    def user(self):
        return self.__user

    @property
    def list(self):
        return self.__list
