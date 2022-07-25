from django.contrib.auth import get_user_model
from django.http import FileResponse, HttpResponse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from asma_asam.permissions import IsSuperUserOrReadOnly, ReadOnly
from words.api.serializers import WordSerializer, WordCategorySerializer, LinkManagerSerializer
from words.models import Word, WordCategory, LinkManager

User = get_user_model()


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


class LinkManagerViewSet(ListAPIView):
    lookup_url_kwarg = 'wid'

    def get_queryset(self):
        link = LinkManager.objects.filter(
            user=self.request.user,
            word=self.kwargs.get('wid')
        )
        if len(link) == 0:
            link = LinkManager.objects.create(
                user=self.request.user,
                word=Word.objects.get(id=self.kwargs.get('wid'))
            )
            link.generate_link()
            link.save()
            link = link.get_queryset()
        return link

    serializer_class = LinkManagerSerializer
    permission_classes = [ReadOnly]


def video_url(request, token, lid):
    lid = force_str(urlsafe_base64_decode(lid))
    link = LinkManager.objects.get(id=lid)
    path = request.build_absolute_uri()
    if link.check_link(token, path):
        response = FileResponse(open(link.word.video.path, 'rb'))
    else:
        response = HttpResponse(status=403)
    link.generate_link()
    return response
