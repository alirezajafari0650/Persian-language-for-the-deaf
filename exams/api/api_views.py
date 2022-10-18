import random

from rest_framework.viewsets import ModelViewSet
from asma_asam.permissions import IsProfessionalUser
from exams.api.serializers import ExamSerializer
from exams.models import Exam
from words.models import Word
from words.api.serializers import WordSerializer

def get_exam(last_id):
    exam = Exam.objects.filter(id=random.randint(1, last_id))
    if len(exam) == 0:
        return get_exam(last_id)
    return exam


class ExamViewSet(ModelViewSet):
    def get_queryset(self):
        exams = Exam.objects.all()
        exams_count = 174
        exam = exams[random.choice(range(exams_count))]
        start_word = exam.start_word
        end_word = exam.end_word
        exam_options = random.sample(range(start_word, end_word + 1), k=4)
        words = Word.objects.filter(id__in=exam_options)
        return words

    serializer_class = WordSerializer
    permission_classes = [IsProfessionalUser]

# class ExamViewSet(ModelViewSet):
#     def get_queryset(self):
#         last_id = Exam.objects.latest('id').id
#         return get_exam(last_id)
#
#     serializer_class = ExamSerializer
#     permission_classes = [IsProfessionalUser]
