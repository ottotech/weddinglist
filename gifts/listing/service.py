# Python imports
from abc import ABC
from abc import abstractmethod


class StorageABC(ABC):
    @abstractmethod
    def get_all_products(self):
        pass

    @abstractmethod
    def get_all_added_gifts(self):
        pass


class Lister(StorageABC):
    __slots__ = [
        "__storage"
    ]

    def __init__(self, storage):
        self.__storage = storage

    def get_all_products(self):
        self.__storage.get_all_products()

    def get_all_added_gifts(self):
        self.__storage.get_all_added_gifts()
