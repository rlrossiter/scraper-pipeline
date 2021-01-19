import time
import typing

from scraper_pipeline.models import notification
from scraper_pipeline.models import state_change_notification
from scraper_pipeline.models import subscriber


class Notifier(object):
    """
    Notifies subscribers on state change
    """

    def __init__(self, notify_callable: typing.Callable[[str, str, str, str, typing.Dict[str, str]], typing.NoReturn]):
        self._call = notify_callable

    def notify_change(self,
                      state_change: state_change_notification.StateChangeNotification,
                      past_notifications: typing.List[notification.Notification],
                      subscribers: typing.List[subscriber.Subscriber]) -> typing.List[notification.Notification]:

        relevant_notifications = [n for n in past_notifications
                                  if n.page_id == state_change.page_id]
        new_notifications = []

        for sub in [s for s in subscribers if s.page_id == state_change.page_id]:
            # find all subscribers listening on this page_id
            # and only find subscribers where they were last notified
            # past their wait time
            has_recent_notification = [n for n in relevant_notifications
                                       if n.address == sub.address
                                       and n.last_notify_time + sub.wait_seconds > int(time.time())]
            if not has_recent_notification:
                self._call(
                    state_change.page_id,
                    state_change.old_state,
                    state_change.new_state,
                    sub.address,
                    state_change.metadata)
                new_notifications.append(notification.Notification(
                    page_id=state_change.page_id,
                    address=sub.address,
                    last_notify_time=int(time.time())
                ))

        return new_notifications
