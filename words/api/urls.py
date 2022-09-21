from django.urls import path
from rest_framework.routers import DefaultRouter

from words.api.api_views import WordCategoryViewSet, WordViewSet, NewWordView, LinkManagerView, video_url, test

app_name = 'words-api'
router = DefaultRouter()
router.register(r'words', WordViewSet, basename='word')
router.register(r'word-categories', WordCategoryViewSet, basename='word-category')
router.register(r'new-words', NewWordView, basename='new-word')
urlpatterns = router.urls
urlpatterns += [
    path('video/<token>/<lid>/<video_number>/', video_url, name='video_url'),
    path('link-managers/<int:wid>/', LinkManagerView.as_view(), name='link-manager'),
    path('test/', test)
]
