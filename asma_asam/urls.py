from azbankgateways.urls import az_bank_gateways_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from words.api.api_views import video_url

urlpatterns = [
                  path('jafar_mola/', admin.site.urls),
                  path('word-api/', include('words.api.urls')),
                  path('affair-api/', include('affairs.api.urls')),
                  path('kernel-api/', include('kernel.api.urls')),
                  path('video/<token>/<lid>/', video_url),
                  path('auth/', include('drf_sms_auth.api.urls')),
                  path('bankgateways/', az_bank_gateways_urls()),
                  path('__debug__/', include('debug_toolbar.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
