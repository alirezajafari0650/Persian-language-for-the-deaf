from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import AuthAPIView, EntryAPIView, ChangePhoneNumberAPIView

urlpatterns = [
    path('sign-in/', EntryAPIView.as_view()),
    path('auth/', AuthAPIView.as_view()),
    path('change-phonenumber/', ChangePhoneNumberAPIView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('verify/', TokenVerifyView.as_view()),
]
