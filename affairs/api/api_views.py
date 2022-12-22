from django.http import FileResponse, HttpResponse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from affairs.api.serializers import AffairSerializer, AffairCategorySerializer
from affairs.models import Affair, AffairCategory, AffairLinkManager
from asma_asam.permissions import IsProfessionalUser


def get_link(user, word_id):
    affair = Affair.objects.get(id=word_id)
    link = AffairLinkManager.objects.create(
        user=user,
        affair=affair
    )
    link.generate_link()
    link.save()
    link = link.link
    return [{
        'link': link,
    }]


class AffairViewSet(ModelViewSet):
    queryset = Affair.objects.all()
    serializer_class = AffairSerializer
    permission_classes = [IsProfessionalUser]
    filter_fields = ['category__farsi_name']
    search_fields = ['farsi_description']
    ordering = ['sort_id']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action != 'retrieve':
            context['fields'] = ['id', 'farsi_description']

        return context

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
            if request.user.is_authenticated and request.user.is_professional and 'video_link' in \
                    self.get_serializer_context()['fields']:
                for item in data:
                    if not item['video_link']:
                        item['video_link'] = get_link(request.user, item['id'])

            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AffairCategoryViewSet(ModelViewSet):
    queryset = AffairCategory.objects.all()
    serializer_class = AffairCategorySerializer
    permission_classes = [IsProfessionalUser]
    filter_fields = ['parent__farsi_name']
    ordering = ['sort_id']
    search_fields = ['farsi_name']

    def get_queryset(self):
        if self.action == 'list':
            queryparams = self.request.query_params
            parent__farsi_name = queryparams.get('parent__farsi_name')
            if parent__farsi_name:
                return AffairCategory.objects.filter(parent__farsi_name=parent__farsi_name)
            return AffairCategory.objects.filter(parent__farsi_name=None).exclude(farsi_name=None)
        return AffairCategory.objects.all()


def affair_video_url(request, token, lid):
    lid = force_str(urlsafe_base64_decode(lid))
    link = AffairLinkManager.objects.get(id=lid)
    path = request.build_absolute_uri()
    if link.check_link(token, path):
        video = link.affair.video
        response = FileResponse(open(video.path, 'rb'))
    else:
        response = HttpResponse(status=403)
    return response
