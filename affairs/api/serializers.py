from rest_framework import serializers

from affairs.models import Affair, AffairCategory, AffairLinkManager
from asma_asam.dynamic_fields import DynamicFieldsMixin


class AffairCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AffairCategory
        fields = '__all__'


class AffairLinkManagerSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()

    class Meta:
        model = AffairLinkManager
        fields = ['link']

    def get_link(self, obj):
        if obj.link and obj.user == self.context['request'].user:
            return obj.link


class AffairSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    video_link = serializers.SerializerMethodField()
    like = serializers.SerializerMethodField()

    class Meta:
        model = Affair
        exclude = ['video']

    def get_like(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.like.filter(user=user).exists()
        else:
            return False

    def get_video_link(self, obj):
        user = self.context['request'].user
        if user.is_authenticated and user.is_professional:
            obj = obj.video_link.filter(user=user).first()
            if obj:
                return AffairLinkManagerSerializer(obj, context=self.context).data
