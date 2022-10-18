import random

from django.contrib.auth import get_user_model
from django.http import FileResponse, HttpResponse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.decorators import action
from rest_framework.mixins import DestroyModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet

from asma_asam.permissions import IsSuperUserOrReadOnly, IsProfessionalUser
from words.api.serializers import WordSerializer, WordCategorySerializer, NewWordSerializer
from words.models import Word, WordCategory, LinkManager, NewWord, Exam

User = get_user_model()


def get_link(user, word_id):
    word = Word.objects.get(id=word_id)
    link = LinkManager.objects.create(
        user=user,
        word=word
    )
    link.generate_link()
    link.save()
    link = link.link
    if word.video1:
        video1 = link + '1/'
    else:
        video1 = None
    if word.video2:
        video2 = link + '2/'
    else:
        video2 = None
    return [{
        'link': link,
        'video1': video1,
        'video2': video2
    }]


class WordCategoryViewSet(ModelViewSet):
    serializer_class = WordCategorySerializer
    permission_classes = [IsSuperUserOrReadOnly]
    filter_fields = ['parent__farsi_name']
    ordering = ['sort_id']
    search_fields = ['@farsi_name']

    def get_queryset(self):
        queryparams = self.request.query_params
        parent__farsi_name = queryparams.get('parent__farsi_name')
        if parent__farsi_name:
            return WordCategory.objects.filter(parent__farsi_name=parent__farsi_name)
        return WordCategory.objects.filter(parent__farsi_name=None).exclude(farsi_name=None)


class WordViewSet(ModelViewSet):
    serializer_class = WordSerializer
    permission_classes = [IsSuperUserOrReadOnly]
    filter_fields = ['category__farsi_name']
    search_fields = ['farsi_name', 'farsi_description', 'farsi_description2']
    ordering = ['sort_id']

    def get_queryset(self):
        queryparams = self.request.query_params
        words = queryparams.get('words')
        if words:
            words = words.split(',')
            return Word.objects.filter(id__in=words).prefetch_related('video_link')
        return Word.objects.all().prefetch_related('video_link')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        if request.user.is_authenticated and request.user.is_professional:
            if not data['video_link']:
                data['video_link'] = get_link(request.user, instance.id)
        return Response(data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = serializer.data
            if request.user.is_authenticated and request.user.is_professional:
                for item in data:
                    if not item['video_link']:
                        item['video_link'] = get_link(request.user, item['id'])

            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class NewWordView(ListModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = NewWord.objects.all()
    serializer_class = NewWordSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['POST'])
    def create_or_update(self, request):
        new_word = NewWord.objects.filter(name=request.data.get('name'))
        data = {'name': request.data.get('name')}
        if new_word.exists():
            new_word = new_word.first()
            print(new_word.user.all().values_list('id', flat=True))
            data['user'] = list(new_word.user.all().values_list('id', flat=True)) + [request.user.id]
            print(data)
            serializer = self.get_serializer(new_word, data=data, partial=True)

        else:
            data['user'] = [request.user.id]
            serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ExamViewSet(ModelViewSet):
    serializer_class = WordSerializer
    permission_classes = [IsProfessionalUser]

    def get_queryset(self):
        exams = Exam.objects.all()
        exams_count = 174
        exam = exams[random.choice(range(exams_count))]
        start_word = exam.start_word
        end_word = exam.end_word
        exam_options = random.sample(range(start_word, end_word + 1), k=4)
        words = Word.objects.filter(id__in=exam_options).prefetch_related('video_link')
        return words

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = serializer.data
            if request.user.is_authenticated and request.user.is_professional:
                for item in data:
                    if not item['video_link']:
                        item['video_link'] = get_link(request.user, item['id'])

            return self.get_paginated_response(data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# class LinkManagerView(ListAPIView):
#     serializer_class = LinkManagerSerializer
#     permission_classes = [IsSuperUserOrReadOnly & IsAuthenticated]
#     lookup_url_kwarg = 'wid'
#
#     def get_queryset(self):
#         link = LinkManager.objects.filter(
#             user=self.request.user,
#             word=self.kwargs.get('wid')
#         ).select_related('word')
#
#         if len(link) == 0:
#             link = LinkManager.objects.create(
#                 user=self.request.user,
#                 word=Word.objects.get(id=self.kwargs.get('wid'))
#             )
#             link.generate_link()
#             link.save()
#             link = self.get_queryset()
#         return link


def video_url(request, token, lid, video_number):
    lid = force_str(urlsafe_base64_decode(lid))
    link = LinkManager.objects.get(id=lid)
    path = request.build_absolute_uri()[:-2]
    video_number = str(video_number)
    if link.check_link(token, path, video_number) or 1 == 1:
        video1 = link.word.video1
        video2 = link.word.video2

        if video_number == '1' and video1:
            response = FileResponse(open(video1.path, 'rb'))
        elif video_number == '2' and video2:
            response = FileResponse(open(video2.path, 'rb'))
        else:
            response = HttpResponse(status=403)
    else:
        response = HttpResponse(status=403)

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
