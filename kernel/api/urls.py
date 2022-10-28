from django.urls import path
from rest_framework.routers import DefaultRouter

from kernel.api.api_views import BankGateway, FactureViewSet, AdViewSet, SearchView, LikeViewSet,CustomUserViewSet

app_name = 'kernel-api'
router = DefaultRouter()
router.register('factures', FactureViewSet, basename='factures')
router.register('ads', AdViewSet, basename='ads')
router.register('likes', LikeViewSet, basename='likes')
router.register('users', CustomUserViewSet, basename='users')
urlpatterns = [
    path('bankgateway/', BankGateway.as_view(), name='bankgateway'),
    path('search/', SearchView.as_view(), name='search'),
]
urlpatterns += router.urls
