import random

from rest_framework import serializers
from rest_framework.reverse import reverse_lazy

from exams.models import Exam


class ExamSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = '__all__'

    @staticmethod
    def get_options(obj):
        options = random.sample(range(obj.start_word, obj.end_word + 1), k=4)
        main_url = reverse_lazy('words-api:word-list')
        urls = ['http://localhost:8000' + main_url + str(option) for option in options]
        return urls
