from rest_framework import serializers

from words.models import Word, WordCategory, LinkManager, NewWord


class WordCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WordCategory
        fields = '__all__'


class WordSerializer(serializers.ModelSerializer):
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


class LinkManagerSerializer(serializers.ModelSerializer):
    word = WordSerializer()
    link1 = serializers.SerializerMethodField(read_only=True)
    link2 = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = LinkManager
        fields = ['word', 'user', 'link1', 'link2']

    @staticmethod
    def get_link1(obj):
        return obj.link + '1/'

    @staticmethod
    def get_link2(obj):
        return obj.link + '2/'
