import random

from rest_framework import serializers

from exams.models import Exam
from words.models import LinkManager, Word


class ExamSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = '__all__'

    def option_to_link(self, request, options):
        data = []
        for option in options:

            link = LinkManager.objects.filter(
                user=request.user,
                word=option
            ).select_related('word')
            print(option)
            if len(link) == 0:
                link = LinkManager.objects.create(
                    user=request.user,
                    word=Word.objects.get(id=option)
                )
                link.generate_link()
                link.save()
            else:
                link = link.first()
            data.append(link)
        # return LinkManagerSerializer(data, many=True, context=self.context).data
        return data
    def get_options(self, obj, options=None):
        if options is None:
            options = random.sample(range(obj.start_word, obj.end_word + 1), k=4)
        request = self.context['request']
        try:
            return self.option_to_link(request, options)
        except Exception as e:
            print(e)
            return self.get_options(obj, options)
