import hashlib
import json
from urllib.parse import urljoin

import requests

from ..base import SMSProvider

URL = 'http://gate.smsaero.ru/'
TYPE_SEND = 2


class SmsAeroException(Exception):
    pass


class Smsaero(SMSProvider):
    def _request(self, endpoint, data):
        m = hashlib.md5(self.conf.SMS_PROVIDER_PASSWORD.encode())
        passwd = m.hexdigest()
        data.update({
            'from': self.conf.SMS_PROVIDER_FROM,
            'type_send': TYPE_SEND,
            'digital': 0,
            'user': self.conf.SMS_PROVIDER_LOGIN,
            'password': passwd,
            'answer': 'json',
        })

        url = urljoin(URL, endpoint)

        try:
            response = requests.post(url, data=data)
        except Exception:
            raise SmsAeroException('Error send sms')

        if not response.status_code == 200:
            raise Exception('Response status over 200')

        return json.loads(response.text)

    def send_sms(self):
        phone_number = str(self.to).replace(' ', '') \
            .replace('-', '') \
            .replace('+', '') \
            .replace('(', '') \
            .replace(')', '')

        data = {
            'to': phone_number,
            'text': self.message,
        }
        try:
            return self._request('/send/', data)
        except Exception as e:
            print("Error send sms", data)
