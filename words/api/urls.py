from django.urls import path
from rest_framework.routers import DefaultRouter

from words.api.api_views import WordViewSet, WordCategoryViewSet, LinkManagerViewSet, video_url,test

app_name = 'words-api'
router = DefaultRouter()
router.register(r'words', WordViewSet, basename='word')
router.register(r'word-categories', WordCategoryViewSet, basename='word-category')
urlpatterns = router.urls
urlpatterns += [
    path('video/<token>/<lid>/', video_url, name='video_url'),
    path('link-managers/<int:wid>/', LinkManagerViewSet.as_view(), name='link-manager'),
    path('test/',test)
]
