# Python imports
from abc import ABC
from abc import abstractmethod
import time

# Project imports
from .domain_events import GiftAddedEvent
from .domain_events import GiftCouldNotBeAddedEvent
from .exceptions import NoStockErr


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
        try:
            self.__storage.add_gift_to_user_wedding_list(user_id=user_id, gift_id=gift_id)

            now = time.monotonic()

            return GiftAddedEvent(timestamp=now)

        except NoStockErr:

            now = time.monotonic()
            event = GiftCouldNotBeAddedEvent(timestamp=now)
            event.message = f"gift with id ({gift_id}) is out of stock."

            return event
