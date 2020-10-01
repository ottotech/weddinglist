# Python imports
from abc import ABC
from abc import abstractmethod
import time

# Project imports
from .domain_events import GiftDeletedFromListEvent


class _StorageABC(ABC):
    @abstractmethod
    def remove_gift_from_user_wedding_list(self, user_id: int, gift_id: int):
        pass


class Deleter(_StorageABC):
    __slots__ = [
        "__storage"
    ]

    def __init__(self, storage):
        self.__storage = storage

    def remove_gift_from_user_wedding_list(self, user_id: int, gift_id: int):
        self.__storage.remove_gift_from_user_wedding_list(user_id=user_id, gift_id=gift_id)

        now = time.monotonic()

        return GiftDeletedFromListEvent(timestamp=now)
