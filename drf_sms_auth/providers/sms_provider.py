# from ippanel import Client, HTTPError, Error, ResponseCode
# from drf_sms_auth.providers.base import SMSProvider as BaseSMSProvider
#
#
# class SMSProvider(BaseSMSProvider):
#     def send_sms(self):
#         sms = Client(self.conf.SMS_AUTH_AUTH_TOKEN)
#         try:
#
#             pattern_values = {
#                 "code": self.message.split(':')[1],
#             }
#             print("yyity6bd4hxjssr",
#                   self.conf.SMS_PROVIDER_FROM,
#                   f"{self.to}",
#                   pattern_values
#                   )
#
#             response = sms.send_pattern(
#                 pattern_code="yyity6bd4hxjssr",
#                 originator=self.conf.SMS_PROVIDER_FROM,
#                 recipient=f"{self.to}",
#                 values=pattern_values
#             )
#             print(response)
#         except Error as e:
#             print("Error handled => code: %s, message: %s" % (e.code, e.message))
#             if e.code == ResponseCode.ErrUnprocessableEntity.value:
#                 for field in e.message:
#                     print("Field: %s , Errors: %s" % (field, e.message[field]))
#         except HTTPError as e:
#             print("Error handled => code: %s" % (e))
#
#         # print(self.message)
#         # try:
#         #     api = KavenegarAPI(self.conf.SMS_AUTH_AUTH_TOKEN)
#         #     params = {
#         #         'sender': self.conf.SMS_PROVIDER_FROM,
#         #         'receptor': f"{self.to}",
#         #         'message': 'کد تایید :'+self.message.split(':')[1]
#         #     }
#         #     response = api.sms_send(params)
#         #     print(response)
#         #     return response
#         # except APIException as e:
#         #     print(e)
#         #     return e
#         # except HTTPException as e:
#         #     print(e)
#         #     return e
#
#
# Sms_Provider = SMSProvider
