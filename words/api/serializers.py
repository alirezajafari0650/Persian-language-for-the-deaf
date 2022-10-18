from drf_dynamic_fields import DynamicFieldsMixin
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

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
        if obj.link:
            return obj.link
        else:
            return 'None'

    def get_video1(self, obj):
        if IsProfessionalUser().has_permission(self.context['request'], self) and obj.word.video1:
            return obj.link + '1/'
        else:
            return None

    def get_video2(self, obj):
        if IsProfessionalUser().has_permission(self.context['request'], self) and obj.word.video2:
            return obj.link + '2/'
        else:
            return None


class WordSerializer(DynamicFieldsMixin, WritableNestedModelSerializer):
    video_link = LinkManagerSerializer(many=True, read_only=True)

    class Meta:
        model = Word
        exclude = ['video1', 'video2']


class NewWordSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = NewWord
        fields = ['name', 'user', 'count']

    @staticmethod
    def get_count(obj):
        return obj.user.count()

# class LinkManagerSerializer(serializers.ModelSerializer):
#     word = WordSerializer()
#     link1 = serializers.SerializerMethodField(read_only=True)
#     link2 = serializers.SerializerMethodField(read_only=True)
#
#     class Meta:
#         model = LinkManager
#         fields = ['word', 'user', 'link1', 'link2']
#
#     @staticmethod
#     def get_link1(obj):
#         return obj.link + '1/'
#
#     @staticmethod
#     def get_link2(obj):
#         return obj.link + '2/'
