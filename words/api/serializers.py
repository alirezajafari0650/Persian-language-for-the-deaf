from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from asma_asam.dynamic_fields import DynamicFieldsMixin
from asma_asam.permissions import IsProfessionalUser
from words.models import Word, WordCategory, LinkManager, NewWord


class WordCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WordCategory
        fields = '__all__'


class LinkManagerSerializer(serializers.ModelSerializer):
    video1 = serializers.SerializerMethodField()
    video2 = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()

    class Meta:
        model = LinkManager
        fields = ['link', 'video1', 'video2']

    def get_link(self, obj):
        if obj.link and obj.user == self.context['request'].user:
            return obj.link

    def get_video1(self, obj):
        if IsProfessionalUser().has_permission(self.context['request'], self) and obj.word.video1 and obj.user == \
                self.context['request'].user:
            return obj.link + '1/'
        else:
            return None

    def get_video2(self, obj):
        if IsProfessionalUser().has_permission(self.context['request'], self) and obj.word.video2 and obj.user == \
                self.context['request'].user:
            return obj.link + '2/'
        else:
            return None


class WordSerializer(DynamicFieldsMixin, WritableNestedModelSerializer):
    video_link = serializers.SerializerMethodField()
    like = serializers.SerializerMethodField()

    class Meta:
        model = Word
        exclude = ['video1', 'video2']

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
                return LinkManagerSerializer(obj, context=self.context).data


class NewWordSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = NewWord
        fields = ['id', 'name', 'user', 'count', 'is_added']

    @staticmethod
    def get_count(obj):
        return obj.user.count()
