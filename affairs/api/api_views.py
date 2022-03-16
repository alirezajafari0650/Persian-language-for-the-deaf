from rest_framework.viewsets import ModelViewSet

from affairs.api.serializers import AffairSerializer, AffairCategorySerializer
from affairs.models import Affair, AffairCategory
from asma_asam.permissions import IsSuperUserOrReadOnly


class AffairViewSet(ModelViewSet):
    queryset = Affair.objects.all()
    serializer_class = AffairSerializer
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


class AffairCategoryViewSet(ModelViewSet):
    queryset = AffairCategory.objects.all()
    serializer_class = AffairCategorySerializer
    permission_classes = [IsSuperUserOrReadOnly]
    filter_fields = ['parent']
    ordering = ['-sort_id']
