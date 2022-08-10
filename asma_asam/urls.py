from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from sms_auth.api.views import EntryAPIView, ChangePhoneNumberAPIView
from kernel.api.api_view import AuthAPIView
from words.api.api_views import video_url

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('word-api/', include('words.api.urls')),
                  path('affair-api/', include('affairs.api.urls')),
                  path('exam-api/', include('exams.api.urls')),
                  path('video/<token>/<lid>/', video_url),
                  # path('auth/', include('sms_auth.api.urls')),
                  path('auth/refresh/', TokenRefreshView.as_view()),
                  path('auth/verify/', TokenVerifyView.as_view()),
                  path('auth/sign-in/', EntryAPIView.as_view()),
                  path('auth/auth/', AuthAPIView.as_view()),
                  path('auth/change-phonenumber/', ChangePhoneNumberAPIView.as_view()),
                  path('__debug__/', include('debug_toolbar.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

