from django.contrib.auth import get_user_model
from sms_auth.api.exceptions import SMSCodeNotFoundException
from sms_auth.api.views import AuthAPIView as BaseAuthAPIView
from sms_auth.conf import conf
from sms_auth.models import PhoneCode
from sms_auth.services.auth import AuthService as BaseAuthService

User = get_user_model()


class AuthService(BaseAuthService):

    def process(self):
        generated_code = PhoneCode.objects. \
            filter(phone_number=self.phone_number,
                   code=self.code) \
            .first()

        if generated_code is None:
            raise SMSCodeNotFoundException()

        user = generated_code.owner
        is_created = False
        kwargs = {'username': generated_code.phone_number}
        if user is None:
            user, is_created = User.objects.get_or_create(**kwargs,
                                                          defaults={"is_active": True})
        else:
            user.username = generated_code.phone_number
            user.save()

        generated_code.delete()

        return user, is_created


class AuthAPIView(BaseAuthAPIView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data.get("phone_number")
            code = serializer.validated_data.get("code")
            user, is_created = AuthService.execute(phone_number=phone_number, code=code)
            self.after_auth(user=user, is_created=is_created)
            serializer = self.get_response_serializer()
            success_value = serializer(instance=user, context={'request': request}).data

            return self.success_objects_response(success_value)
        else:
            return self.error_response(serializer.errors)
