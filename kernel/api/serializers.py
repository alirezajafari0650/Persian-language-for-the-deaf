from django.contrib.auth import get_user_model
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class TokenSerializer(serializers.ModelSerializer):
    refresh = serializers.SerializerMethodField(read_only=True)
    access = serializers.SerializerMethodField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    username = PhoneNumberField(read_only=True)

    # refresh = self.get_token(self.user)
    #
    # data['refresh'] = str(refresh)
    # data['access'] = str(refresh.access_token)
    class Meta:
        model = User
        fields = ['id', 'username', 'refresh', 'access']

    def get_refresh(self, obj):
        user = self.instance
        refresh = TokenObtainPairSerializer.get_token(user)
        return str(refresh)

    def get_access(self, obj):
        user = self.instance
        refresh = TokenObtainPairSerializer.get_token(user)
        return str(refresh.access_token)
