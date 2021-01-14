import typing


class StateChangeNotification(typing.NamedTuple):
    page_id: str
    old_state: str
    new_state: str
    metadata: typing.Dict[str, str] = None
