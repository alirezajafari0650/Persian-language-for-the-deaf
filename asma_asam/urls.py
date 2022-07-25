from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from words.api.api_views import video_url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('word-api/', include('words.api.urls')),
    path('affair-api/', include('affairs.api.urls')),
    path('exam-api/', include('exams.api.urls')),
    path('video/<token>/<lid>/', video_url, name='video_url'),

]
