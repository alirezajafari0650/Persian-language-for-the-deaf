from rest_framework import serializers

from words.models import Word, WordCategory


class WordCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WordCategory
        fields = '__all__'


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = '__all__'
