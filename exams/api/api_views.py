import random

from rest_framework.viewsets import ModelViewSet

from exams.api.serializers import ExamSerializer
from exams.models import Exam


def get_exam(last_id):
    exam = Exam.objects.filter(id=random.randint(1, last_id))
    if len(exam) == 0:
        return get_exam(last_id)
    return exam


class ExamViewSet(ModelViewSet):
    def get_queryset(self):
        last_id = Exam.objects.latest('id').id
        return get_exam(last_id)

    serializer_class = ExamSerializer
