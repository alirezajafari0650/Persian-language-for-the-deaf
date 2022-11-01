import logging

from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.http import Http404
from django.urls import reverse
from drf_excel.mixins import XLSXFileMixin
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from affairs.api.api_views import AffairViewSet
from asma_asam.permissions import IsSuperUser, IsSuperUserOrReadOnly
from kernel.api.serializers import FactureSerializer, AdSerializer, LikeSerializer, CustomUserSerializer, \
    SuperUserOrProfessionalSerializer
from kernel.models import Facture, CustomUser, Ad, Like
from words.api.api_views import WordViewSet


class BankGateway(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        amount = 20000
        user_mobile_number = request.user.username
        factory = bankfactories.BankFactory()
        try:
            bank = factory.create()
            bank.set_request(request)
            bank.set_amount(amount)
            bank.set_client_callback_url(reverse('kernel-api:bankgateway'))
            bank.set_mobile_number(user_mobile_number)
            bank_record = bank.ready()
            return bank.redirect_gateway()
        except AZBankGatewaysException as e:
            logging.critical(e)
            return Response({'error': str(e)})

    @staticmethod
    def get(request):
        tracking_code = request.query_params.get(settings.TRACKING_CODE_QUERY_PARAM, None)
        if not tracking_code:
            raise Http404

        try:
            bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
        except bank_models.Bank.DoesNotExist:
            raise Http404

        if bank_record.is_success:
            user = CustomUser.objects.get(id=request.user.id)
            user.is_professional = True
            user.save()
            Facture.objects.create(user=user, price=bank_record.amount)
            return Response({'message': "پرداخت با موفقیت انجام شد."})

        return Response({
            'message': "پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت."})


class FactureViewSet(XLSXFileMixin, ReadOnlyModelViewSet):
    permission_classes = [IsSuperUser]
    queryset = Facture.objects.all().select_related('user')
    serializer_class = FactureSerializer
    filter_fields = {'date': ['range']}
    filename = 'گزارش_مالی.xlsx'


class AdsViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


class SearchView(APIView):
    def get(self, request):
        return_data = {}
        query = request.query_params.get('search', None)
        if query:
            return_data['words'] = WordViewSet.as_view({'get': 'list'})(request._request).data.get('results', [])
            return_data['affairs'] = AffairViewSet.as_view({'get': 'list'})(request._request).data.get('results', [])
        return Response(return_data)


class LikeViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def add_like(self, request):
        word_id = request.data.get('word_id', None)
        affair_id = request.data.get('affair_id', None)
        like, created = Like.objects.get_or_create(user=request.user)
        if word_id:
            like.liked_words.add(word_id)
        if affair_id and request.user.is_professional:
            like.liked_affair.add(affair_id)
        return Response({'message': 'به لیست علاقه مندی ها اضافه شد.'})

    @action(detail=False, methods=['post'])
    def delete_like(self, request):
        word_id = request.data.get('word_id', None)
        affair_id = request.data.get('affair_id', None)
        like = Like.objects.get(user=request.user)
        if word_id:
            like.liked_words.remove(word_id)
        if affair_id:
            like.liked_affair.remove(affair_id)
        return Response({'message': 'از لیست علاقه مندی ها حذف شد.'})


class CustomUserViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsSuperUser]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=True, methods=['POST'])
    def change_status(self, request, pk=None):
        serializer = SuperUserOrProfessionalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_professional = serializer.validated_data.get('is_professional')
        is_superuser = serializer.validated_data.get('is_superuser')
        user = self.get_object()
        user.is_professional = is_professional
        user.is_superuser = is_superuser
        user.save()
        return Response({'message': 'عملیات با موفقیت انجام شد.'})
