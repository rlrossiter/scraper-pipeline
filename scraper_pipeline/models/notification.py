import typing


class Notification(typing.NamedTuple):
    page_id: str
    address: str
    last_notify_time: int
