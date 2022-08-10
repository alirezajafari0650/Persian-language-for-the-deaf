from kavenegar import *
from sms_auth.providers.base import SMSProvider as BaseSMSProvider


class SMSProvider(BaseSMSProvider):
    def send_sms(self):
        print(self.message)
        try:
            api = KavenegarAPI(self.conf.SMS_AUTH_AUTH_TOKEN)
            params = {
                'sender': self.conf.SMS_PROVIDER_FROM,
                'receptor': f"{self.to}",
                'message': 'کد تایید :'+self.message.split(':')[1]
            }
            response = api.sms_send(params)
            print(response)
            return response
        except APIException as e:
            print(e)
            return e
        except HTTPException as e:
            print(e)
            return e


Sms_Provider = SMSProvider
