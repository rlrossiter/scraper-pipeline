import contextlib
from email import message
import smtplib

from scraper_pipeline.exception import connection_exception

GMAIL_SMTP_ADDR = 'smtp.gmail.com'
GMAIL_SMTP_PORT = 465


class GmailNotifier(object):

    def __init__(self, email, password):
        self._email = email
        self._password = password
        self._server_conn = None

    @contextlib.contextmanager
    def connect(self):
        self._server_conn = self._connect_server()

        try:
            yield self
        finally:
            self._server_conn.quit()
            self._server_conn = None

    def send(self, to, subject, body):
        if not self._server_conn:
            raise connection_exception.ConnectionNotEstablishedException()

        msg = message.EmailMessage()
        msg['To'] = to
        msg['Subject'] = subject
        msg.set_content(body)

        self._server_conn.send_message(msg)

    def _connect_server(self):
        server = smtplib.SMTP_SSL(GMAIL_SMTP_ADDR, GMAIL_SMTP_PORT)
        server.ehlo()
        server.login(self._email, self._password)
        return server
