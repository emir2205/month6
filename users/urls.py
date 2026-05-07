from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import (
    AuthorizationAPIView,
    ConfirmUserAPIView,
    CustomTokenObtainPairView,
    RegistrationAPIView,
)

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view()),
    path('authorization/', AuthorizationAPIView.as_view()),
    path('confirm/', ConfirmUserAPIView.as_view()),
    path('token/', CustomTokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
