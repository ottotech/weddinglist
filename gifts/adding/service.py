# Python imports
from abc import ABC
from abc import abstractmethod


class _StorageABC(ABC):
    @abstractmethod
    def add_gift_to_user_wedding_list(self, user_id: int, gift_id: int):
        pass


class Adder(_StorageABC):
    __slots__ = [
        "__storage"
    ]

    def __init__(self, storage):
        self.__storage = storage

    def add_gift_to_user_wedding_list(self, user_id: int, gift_id: int):
        self.__storage.add_gift_to_user_wedding_list(user_id=user_id, gift_id=gift_id)
