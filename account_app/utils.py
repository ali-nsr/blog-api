import threading
from django.core.mail import send_mail
import time


class SendEmailThread(threading.Thread):
    def __init__(self, subject, msg, from_email, to):
        threading.Thread.__init__(self)
        self.subject = subject
        self.msg = msg
        self.from_email = from_email
        self.to = to

    def run(self):
        send_mail(
            self.subject,
            self.msg,
            self.from_email,
            self.to
        )
