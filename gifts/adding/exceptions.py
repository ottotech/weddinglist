class Error(Exception):
    pass


class DuplicatedErr(Error):
    pass


class NoStockErr(Error):
    pass


class GuestDuplicatedErr(Error):
    pass


class GuestUsernameDuplicatedErr(Error):
    pass
