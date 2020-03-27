import threading

import mailchimp
from django.conf import settings


class SendSubscribeMail(object):
    def __init__(self, email):
        self.email = email
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        print(f'Sending mail to {self.email}')
        api = mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)
        try:
            api.lists.subscribe(settings.MAILCHIMP_SUBSCRIBE_LIST_ID, {'email': self.email})
        except:
            return False
