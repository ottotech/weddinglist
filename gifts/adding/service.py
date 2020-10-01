# Python imports
from abc import ABC
from abc import abstractmethod
import time

# Project imports
from .domain_events import GiftAddedEvent
from .domain_events import GiftCouldNotBeAddedEvent
from .domain_events import GuestAddedEvent
from .exceptions import NoStockErr


class _StorageABC(ABC):
    @abstractmethod
    def add_gift_to_user_wedding_list(self, user_id: int, gift_id: int):
        pass

    @abstractmethod
    def add_guest(self,
                  user_id: int,
                  first_name: str,
                  last_name: str,
                  username: str,
                  password: str):
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

    def add_guest(self,
                  user_id: int,
                  first_name: str,
                  last_name: str,
                  username: str,
                  password: str):

        self.__storage.add_guest(user_id=user_id,
                                 first_name=first_name,
                                 last_name=last_name,
                                 username=username,
                                 password=password)

        now = time.monotonic()
        event = GuestAddedEvent(timestamp=now)
        event.message = f"user with id ({user_id}) successfully added a guest."

        return event
