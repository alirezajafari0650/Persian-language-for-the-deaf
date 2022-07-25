from rest_framework import serializers

from words.models import Word, WordCategory, LinkManager


class WordCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WordCategory
        fields = '__all__'


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = '__all__'


class LinkManagerSerializer(serializers.ModelSerializer):
    word = WordSerializer()

    class Meta:
        model = LinkManager
        fields = '__all__'
