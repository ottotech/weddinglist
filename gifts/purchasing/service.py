# Python imports
from abc import ABC
from abc import abstractmethod
import time

# Project imports
from .domain_events import GiftPurchasedEvent


class _StorageABC(ABC):

    @abstractmethod
    def purchase_gift(self, guest_id: int, gift_id: int, user_id_of_wedding_list: int):
        pass


class Purchaser(_StorageABC):
    __slots__ = [
        "__storage"
    ]

    def __init__(self, storage):
        self.__storage = storage

    def purchase_gift(self, guest_id: int, gift_id: int, user_id_of_wedding_list: int):
        self.__storage.purchase_gift(
            guest_id=guest_id,
            gift_id=gift_id,
            user_id_of_wedding_list=user_id_of_wedding_list
        )

        now = time.monotonic()
        event = GiftPurchasedEvent(timestamp=now)
        event.message = f"guest ({guest_id} purchased gift {gift_id})"

        return event
