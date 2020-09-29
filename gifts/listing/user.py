
class User(object):

    __slots__ = [
        "__user_id",
        "__name",
        "__last_name",
        "__email",
    ]

    def __init__(self, user_id: int, name: str, last_name: str, email: str):
        self.__user_id = user_id
        self.__name = name
        self.__last_name = last_name
        self.__email = email

    @property
    def user_id(self):
        return self.__user_id

    @property
    def name(self):
        return self.__name

    @property
    def last_name(self):
        return self.__last_name

    @property
    def email(self):
        return self.__email
