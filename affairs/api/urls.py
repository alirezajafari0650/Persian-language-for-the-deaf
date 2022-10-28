from django.urls import path
from rest_framework.routers import DefaultRouter

from affairs.api.api_views import AffairViewSet, AffairCategoryViewSet, affair_video_url

app_name = 'affair-api'
router = DefaultRouter()
router.register(r'affairs', AffairViewSet, basename='affair')
router.register(r'affair-categories', AffairCategoryViewSet, basename='affair-category')
urlpatterns = router.urls
urlpatterns += [
    path('affair_video/<token>/<lid>/', affair_video_url, name='affair_video_url'),
]
