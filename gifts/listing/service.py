# Python imports
from abc import ABC
from abc import abstractmethod
from typing import List

# Project imports
from gifts.listing import Gift
from gifts.listing import UserWeddingList


class StorageABC(ABC):
    @abstractmethod
    def get_all_gifts_available(self) -> List[Gift]:
        pass

    @abstractmethod
    def get_user_wedding_list(self, user_id: int) -> UserWeddingList:
        pass


class Lister(StorageABC):

    __slots__ = [
        "__storage"
    ]

    def __init__(self, storage):
        self.__storage = storage

    def get_all_gifts_available(self) -> List[Gift]:
        return self.__storage.get_all_gifts_available()

    def get_user_wedding_list(self, user_id: int) -> UserWeddingList:
        return self.__storage.get_user_wedding_list(user_id=user_id)
