from unittest import mock

import pytest

from scraper_pipeline.models import notification
from scraper_pipeline.models import state_change_notification
from scraper_pipeline.models import subscriber
from scraper_pipeline.notify import notifier as notifier_mod


class TestNotifications(object):
    @mock.patch('time.time', mock.MagicMock(return_value=5000))
    def test_one_subscriber_zero_past_no_metadata(self):
        notif = state_change_notification.StateChangeNotification(page_id='1234', old_state='old', new_state='new')
        sub = subscriber.Subscriber(page_id='1234', address='test', wait_seconds=500)
        mock_call = mock.Mock()

        notifier = notifier_mod.Notifier(mock_call)
        new_notif = notifier.notify_change(notif, [], [sub])

        assert len(new_notif) == 1
        assert new_notif[0] == notification.Notification(page_id='1234', address='test', last_notify_time=5000)
        mock_call.assert_called_once_with('1234', 'old', 'new', 'test', None)

    @mock.patch('time.time', mock.MagicMock(return_value=5000))
    def test_one_subscriber_zero_past_with_metadata(self):
        metadata = {'foo': 'bar'}
        notif = state_change_notification.StateChangeNotification(page_id='1234', old_state='old', new_state='new', metadata=metadata)
        sub = subscriber.Subscriber(page_id='1234', address='test', wait_seconds=500)
        mock_call = mock.Mock()

        notifier = notifier_mod.Notifier(mock_call)
        new_notif = notifier.notify_change(notif, [], [sub])

        assert len(new_notif) == 1
        assert new_notif[0] == notification.Notification(page_id='1234', address='test', last_notify_time=5000)
        mock_call.assert_called_once_with('1234', 'old', 'new', 'test', metadata)

    @mock.patch('time.time', mock.MagicMock(return_value=5000))
    def test_one_subscriber_recent_past(self):
        notif = state_change_notification.StateChangeNotification(page_id='1234', old_state='old', new_state='new')
        sub = subscriber.Subscriber(page_id='1234', address='test', wait_seconds=500)
        recent = notification.Notification(page_id='1234', address='test', last_notify_time=4800)
        mock_call = mock.Mock()

        notifier = notifier_mod.Notifier(mock_call)
        new_notif = notifier.notify_change(notif, [recent], [sub])

        assert not new_notif
        mock_call.assert_not_called()

    @mock.patch('time.time', mock.MagicMock(return_value=5000))
    def test_one_subscriber_old_past(self):
        notif = state_change_notification.StateChangeNotification(page_id='1234', old_state='old', new_state='new')
        sub = subscriber.Subscriber(page_id='1234', address='test', wait_seconds=500)
        recent = notification.Notification(page_id='1234', address='test', last_notify_time=4000)
        mock_call = mock.Mock()

        notifier = notifier_mod.Notifier(mock_call)
        new_notif = notifier.notify_change(notif, [recent], [sub])

        assert len(new_notif) == 1
        assert new_notif[0] == notification.Notification(page_id='1234', address='test', last_notify_time=5000)
        mock_call.assert_called_once_with('1234', 'old', 'new', 'test', None)

    @mock.patch('time.time', mock.MagicMock(return_value=5000))
    def test_one_subscriber_recent_with_different_page_id(self):
        notif = state_change_notification.StateChangeNotification(page_id='5678', old_state='old', new_state='new')
        sub1 = subscriber.Subscriber(page_id='1234', address='test', wait_seconds=500)
        sub2 = subscriber.Subscriber(page_id='5678', address='test', wait_seconds=500)
        recent = notification.Notification(page_id='1234', address='test', last_notify_time=4800)
        mock_call = mock.Mock()

        notifier = notifier_mod.Notifier(mock_call)
        new_notif = notifier.notify_change(notif, [recent], [sub1, sub2])

        assert len(new_notif) == 1
        assert new_notif[0] == notification.Notification(page_id='5678', address='test', last_notify_time=5000)
        mock_call.assert_called_once_with('5678', 'old', 'new', 'test', None)

    @mock.patch('time.time', mock.MagicMock(return_value=5000))
    def test_multiple_subscribers_zero_past(self):
        notif = state_change_notification.StateChangeNotification(page_id='1234', old_state='old', new_state='new')
        sub1 = subscriber.Subscriber(page_id='1234', address='test', wait_seconds=500)
        sub2 = subscriber.Subscriber(page_id='1234', address='test2', wait_seconds=500)
        mock_call = mock.Mock()

        notifier = notifier_mod.Notifier(mock_call)
        new_notif = notifier.notify_change(notif, [], [sub1, sub2])

        assert len(new_notif) == 2
        assert notification.Notification(page_id='1234', address='test', last_notify_time=5000) in new_notif
        assert notification.Notification(page_id='1234', address='test2', last_notify_time=5000) in new_notif
        mock_call.assert_any_call('1234', 'old', 'new', 'test', None)
        mock_call.assert_any_call('1234', 'old', 'new', 'test2', None)

    @mock.patch('time.time', mock.MagicMock(return_value=5000))
    def test_multiple_subscribers_one_recent_one_old_past(self):
        notif = state_change_notification.StateChangeNotification(page_id='1234', old_state='old', new_state='new')
        sub1 = subscriber.Subscriber(page_id='1234', address='test', wait_seconds=500)
        sub2 = subscriber.Subscriber(page_id='1234', address='test2', wait_seconds=500)
        recent1 = notification.Notification(page_id='1234', address='test', last_notify_time=4000)
        recent2 = notification.Notification(page_id='1234', address='test2', last_notify_time=4800)
        mock_call = mock.Mock()

        notifier = notifier_mod.Notifier(mock_call)
        new_notif = notifier.notify_change(notif, [recent1, recent2], [sub1, sub2])

        assert len(new_notif) == 1
        assert new_notif[0] == notification.Notification(page_id='1234', address='test', last_notify_time=5000)
        mock_call.assert_called_once_with('1234', 'old', 'new', 'test', None)

    @mock.patch('time.time', mock.MagicMock(return_value=5000))
    def test_multiple_subscribers_all_old(self):
        notif = state_change_notification.StateChangeNotification(page_id='1234', old_state='old', new_state='new')
        sub1 = subscriber.Subscriber(page_id='1234', address='test', wait_seconds=500)
        sub2 = subscriber.Subscriber(page_id='1234', address='test2', wait_seconds=500)
        recent1 = notification.Notification(page_id='1234', address='test', last_notify_time=4000)
        recent2 = notification.Notification(page_id='1234', address='test2', last_notify_time=4000)
        mock_call = mock.Mock()

        notifier = notifier_mod.Notifier(mock_call)
        new_notif = notifier.notify_change(notif, [recent1, recent2], [sub1, sub2])

        assert len(new_notif) == 2
        assert notification.Notification(page_id='1234', address='test', last_notify_time=5000) in new_notif
        assert notification.Notification(page_id='1234', address='test2', last_notify_time=5000) in new_notif
        mock_call.assert_any_call('1234', 'old', 'new', 'test', None)
        mock_call.assert_any_call('1234', 'old', 'new', 'test2', None)

    @mock.patch('time.time', mock.MagicMock(return_value=5000))
    def test_notification_no_subscribers(self):
        notif = state_change_notification.StateChangeNotification(page_id='1234', old_state='old', new_state='new')
        recent1 = notification.Notification(page_id='1234', address='test', last_notify_time=4000)
        recent2 = notification.Notification(page_id='1234', address='test2', last_notify_time=4000)
        mock_call = mock.Mock()

        notifier = notifier_mod.Notifier(mock_call)
        new_notif = notifier.notify_change(notif, [recent1, recent2], [])

        assert not new_notif

    @mock.patch('time.time', mock.MagicMock(return_value=5000))
    def test_notification_error_on_call(self):
        notif = state_change_notification.StateChangeNotification(page_id='1234', old_state='old', new_state='new')
        sub = subscriber.Subscriber(page_id='1234', address='test', wait_seconds=500)
        mock_call = mock.Mock()
        mock_call.side_effect = Exception("Test error")

        notifier = notifier_mod.Notifier(mock_call)

        pytest.raises(Exception, notifier.notify_change, notif, [], [sub])
