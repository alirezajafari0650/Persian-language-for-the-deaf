from rest_framework.routers import DefaultRouter

from exams.api.api_views import ExamViewSet

app_name = 'exams-api'
router = DefaultRouter()
router.register(r'exams', ExamViewSet, basename='exam')
urlpatterns = router.urls
