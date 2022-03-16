from rest_framework import serializers

from affairs.models import Affair, AffairCategory


class AffairCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AffairCategory
        fields = '__all__'


class AffairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affair
        fields = '__all__'
