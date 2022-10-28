import jdatetime
from django.contrib.auth import get_user_model
from rest_framework import serializers

from affairs.api.serializers import AffairSerializer
from kernel.models import Facture, Ad, Like
from words.api.serializers import WordSerializer

User = get_user_model()


class FactureSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    phone_number = serializers.CharField(source="user.username", read_only=True)
    date = serializers.SerializerMethodField()

    class Meta:
        model = Facture
        fields = ['id', 'phone_number', 'user', 'price', 'date']

    @staticmethod
    def get_user(obj):
        return obj.user.get_full_name()

    @staticmethod
    def get_date(obj):
        return jdatetime.datetime.fromgregorian(datetime=obj.date).strftime("%Y/%m/%d %H:%M:%S")


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['id', 'description']


class LikeSerializer(serializers.ModelSerializer):
    liked_words = WordSerializer(many=True, read_only=True)
    liked_affair = AffairSerializer(many=True, read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'liked_words', 'liked_affair']


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'groups', 'user_permissions']


class SuperUserOrProfessionalSerializer(serializers.Serializer):
    is_professional = serializers.BooleanField()
    is_superuser = serializers.BooleanField()
