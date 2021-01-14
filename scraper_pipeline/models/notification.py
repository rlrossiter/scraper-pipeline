import typing

from scraper_pipeline.models import state_change_notification


class Notification(typing.NamedTuple):
    state_change_notification: state_change_notification.StateChangeNotification
    address: str
    last_notify_time: int
