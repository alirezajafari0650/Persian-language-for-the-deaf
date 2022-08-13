from django.contrib.auth import get_user_model
from django.http import FileResponse, HttpResponse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from asma_asam.permissions import IsSuperUserOrReadOnly
from words.api.serializers import WordSerializer, WordCategorySerializer, LinkManagerSerializer
from words.models import Word, WordCategory, LinkManager

User = get_user_model()


class WordViewSet(ModelViewSet):
    serializer_class = WordSerializer
    permission_classes = [IsSuperUserOrReadOnly]
    filter_fields = ['category__farsi_name']
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
    ordering = ['sort_id']

    def get_queryset(self):
        queryparams = self.request.query_params
        words = queryparams.get('words')
        if words:
            words = words.split(',')
            return Word.objects.filter(id__in=words)
        return Word.objects.all()


class WordCategoryViewSet(ModelViewSet):
    serializer_class = WordCategorySerializer
    permission_classes = [IsSuperUserOrReadOnly]
    filter_fields = ['parent__farsi_name']
    ordering = ['sort_id']

    def get_queryset(self):
        queryparams = self.request.query_params
        parent__farsi_name = queryparams.get('parent__farsi_name')
        if parent__farsi_name:
            return WordCategory.objects.filter(parent__farsi_name=parent__farsi_name)
        return WordCategory.objects.filter(parent__farsi_name=None)


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
            link = self.get_queryset()
        return link

    serializer_class = LinkManagerSerializer
    permission_classes = [IsSuperUserOrReadOnly & IsAuthenticated]


def video_url(request, token, lid):
    lid = force_str(urlsafe_base64_decode(lid))
    link = LinkManager.objects.get(id=lid)
    path = request.build_absolute_uri()
    print(path, link.word.video.path)
    if link.check_link(token, path):
        response = FileResponse(open(link.word.video.path, 'rb'))
    else:
        response = HttpResponse(status=403)
    link.generate_link()
    return response


def test(request):
    # mypath = '/mnt/work/code/project/asma_asam/media/videos'
    # f = []
    # for (dirpath, dirnames, filenames) in os.walk(mypath):
    #     f.extend(filenames)
    # words = Word.objects.all()
    # c = 0
    # z = ''
    # for word in words:
    #     vid = str(word.video)
    #     vid = vid[13:]
    #     if vid not in f:
    #         c += 1
    #         z += word.farsi_name + ' , '
    #         print(word.farsi_name)
    # print(z)
    # print(c)
    return HttpResponse('ok')

    # words = Word.objects.all()
    # for word in words:
    #     vid = str(word.video)
    #     # new_video = 'media/images/' + str(vid) + '.mp4'
    #     new_video = vid[:-8]+'.mp4'
    #     word.video = new_video
    #     word.save()
    #
    # return HttpResponse('ok')
    #
    #  mypath = '/mnt/work/code/project/asma_asam/media/videos'
    # f = []
    # b=[]
    # for (dirpath, dirnames, filenames) in os.walk(mypath):
    #     # print(dirpath)
    #     # print(dirnames)
    #     f.extend(filenames)
    # for i in f:
    #     vidi = os.path.join(mypath,i)
    #     j= 'video'+i[5:]
    #     vidj = os.path.join(mypath,j)
    #     os.rename(vidi,vidj)
    #     b.extend(i)
    # return HttpResponse('ok')
    # mypath = '/mnt/work/code/project/asma_asam/media/videos'
    # f = []
    # b=[]
    # for (dirpath, dirnames, filenames) in os.walk(mypath):
    #     # print(dirpath)
    #     # print(dirnames)
    #     f.extend(filenames)
    # for i in f:
    #     os.rename(i, 'video' + i[5:])
    #     b.extend(i)
    #
    # print(f)
    # print(b)
    # return HttpResponse(f)
