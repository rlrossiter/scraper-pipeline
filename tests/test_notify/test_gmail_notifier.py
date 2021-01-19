from unittest import mock

import pytest

from scraper_pipeline.exception import connection_exception
from scraper_pipeline.notify.plugin import gmail_notifier


class TestGmailNotifier(object):
    def test_connect(self):
        gmail = gmail_notifier.GmailNotifier('email', 'password')

        with mock.patch('smtplib.SMTP_SSL') as mock_smtp:
            with gmail.connect():
                pass

        mock_smtp.assert_called_once_with(gmail_notifier.GMAIL_SMTP_ADDR, gmail_notifier.GMAIL_SMTP_PORT)
        mock_smtp.return_value.ehlo.assert_called_once_with()
        mock_smtp.return_value.login.assert_called_once_with('email', 'password')
        mock_smtp.return_value.quit.assert_called_once_with()

    def test_connect_error(self):
        gmail = gmail_notifier.GmailNotifier('email', 'password')

        with mock.patch('smtplib.SMTP_SSL') as mock_smtp:
            mock_smtp.return_value.ehlo.side_effect = Exception("Bad connection")
            pytest.raises(Exception, self._enter_with, gmail)

        mock_smtp.assert_called_once_with(gmail_notifier.GMAIL_SMTP_ADDR, gmail_notifier.GMAIL_SMTP_PORT)
        mock_smtp.return_value.ehlo.assert_called_once_with()
        mock_smtp.return_value.login.assert_not_called()
        mock_smtp.return_value.quit.assert_not_called()

    def test_connect_error_in_context(self):
        gmail = gmail_notifier.GmailNotifier('email', 'password')

        with mock.patch('smtplib.SMTP_SSL') as mock_smtp:
            pytest.raises(Exception, self._enter_with, gmail, exc=Exception("Error"))

        mock_smtp.assert_called_once_with(gmail_notifier.GMAIL_SMTP_ADDR, gmail_notifier.GMAIL_SMTP_PORT)
        mock_smtp.return_value.ehlo.assert_called_once_with()
        mock_smtp.return_value.login.assert_called_once_with('email', 'password')
        mock_smtp.return_value.quit.assert_called_once_with()

    def test_send_not_connected(self):
        gmail = gmail_notifier.GmailNotifier('email', 'password')

        pytest.raises(connection_exception.ConnectionNotEstablishedException, gmail.send, 'to', 'subject', 'body')

    def test_send(self):
        gmail = gmail_notifier.GmailNotifier('email', 'password')

        with mock.patch('smtplib.SMTP_SSL') as mock_smtp, mock.patch('email.message.EmailMessage') as mock_email:
            with gmail.connect():
                gmail.send('to', 'subject', 'body')

        mock_email.return_value.__setitem__.assert_any_call('To', 'to')
        mock_email.return_value.__setitem__.assert_any_call('From', 'email')
        mock_email.return_value.__setitem__.assert_any_call('Subject', 'subject')
        mock_email.return_value.set_content.assert_called_once_with('body')
        mock_smtp.assert_called_once_with(gmail_notifier.GMAIL_SMTP_ADDR, gmail_notifier.GMAIL_SMTP_PORT)
        mock_smtp.return_value.ehlo.assert_called_once_with()
        mock_smtp.return_value.login.assert_called_once_with('email', 'password')
        mock_smtp.return_value.quit.assert_called_once_with()
        mock_smtp.return_value.send_message.assert_called_once_with(mock_email.return_value)

    def test_send_exception(self):
        gmail = gmail_notifier.GmailNotifier('email', 'password')

        with mock.patch('smtplib.SMTP_SSL') as mock_smtp, mock.patch('email.message.EmailMessage'):
            with gmail.connect():
                mock_smtp.return_value.send_message.side_effect = Exception("Send error")
                pytest.raises(Exception, gmail.send, 'to', 'subject', 'body')

        mock_smtp.assert_called_once_with(gmail_notifier.GMAIL_SMTP_ADDR, gmail_notifier.GMAIL_SMTP_PORT)
        mock_smtp.return_value.quit.assert_called_once_with()

    def _enter_with(self, gmail, exc=None):
        with gmail.connect():
            if exc:
                raise exc
