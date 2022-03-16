from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('word-api/', include('words.api.urls')),
    path('affair-api/', include('affairs.api.urls')),
    path('exam-api/', include('exams.api.urls')),
]
