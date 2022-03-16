from rest_framework.routers import DefaultRouter

from words.api.api_views import WordViewSet, WordCategoryViewSet

app_name = 'words-api'
router = DefaultRouter()
router.register(r'words', WordViewSet, basename='word')
router.register(r'word-categories', WordCategoryViewSet, basename='word-category')
urlpatterns = router.urls
