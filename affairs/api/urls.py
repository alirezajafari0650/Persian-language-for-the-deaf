from rest_framework.routers import DefaultRouter

from affairs.api.api_views import AffairViewSet,AffairCategoryViewSet

app_name = 'affair-api'
router = DefaultRouter()
router.register(r'affairs', AffairViewSet, basename='affair')
router.register(r'affair-categories', AffairCategoryViewSet, basename='affair-category')
urlpatterns = router.urls
