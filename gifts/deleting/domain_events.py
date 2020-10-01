
class _DomainEvent(object):
    def __init__(self, timestamp, **kwargs):
        self.__dict__["timestamp"] = timestamp
        self.__dict__.update(kwargs)

    def __setattr__(self, key, value):
        if hasattr(self, key):
            raise AttributeError(
                "{} attributes can be added but not modified. Attribute {!r} "
                "already exists with value {!r}.".format(
                    self.__class__.__name__,
                    key,
                    getattr(self, key)
                )
            )

        self.__dict__[key] = value

    def __eq__(self, other):
        return type(self) == other

    def __ne__(self, other):
        return not self.__eq__(other)


class GiftDeletedFromListEvent(_DomainEvent):
    pass
