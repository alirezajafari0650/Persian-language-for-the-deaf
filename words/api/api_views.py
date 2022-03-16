from rest_framework.viewsets import ModelViewSet

from asma_asam.permissions import IsSuperUserOrReadOnly
from words.api.serializers import WordSerializer, WordCategorySerializer
from words.models import Word, WordCategory

class WordViewSet(ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    permission_classes = [IsSuperUserOrReadOnly]
    filter_fields = [
        'farsi_name',
        'farsi_description',
        'farsi_description2',
        'english_name',
        'english_description',
        'english_description2',
        'arabic_name',
        'arabic_description',
        'arabic_description2',
        'category',
        'category__farsi_name',
    ]
    search_fields = [
        'farsi_name',
        'farsi_description',
        'farsi_description2',
        'english_name',
        'english_description',
        'english_description2',
        'arabic_name',
        'arabic_description',
        'arabic_description2',
    ]
    ordering = ['-sort_id']


class WordCategoryViewSet(ModelViewSet):
    queryset = WordCategory.objects.all()
    serializer_class = WordCategorySerializer
    permission_classes = [IsSuperUserOrReadOnly]
    filter_fields = ['parent']
    ordering = ['-sort_id']