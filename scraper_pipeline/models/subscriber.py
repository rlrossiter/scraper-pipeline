import typing


class Subscriber(typing.NamedTuple):
    page_id: str
    address: str
    wait_seconds: int