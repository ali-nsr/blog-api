from django.urls import path, include
from . import views

# from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

app_name = 'account_app_api_v1'

urlpatterns = [
    # registration
    path('register/', views.RegisterApiView.as_view(), name='register'),
    # change password
    path('change-password/', views.ChangePasswordApiView.as_view(), name='change_password'),
    # verification
    path('verification/confirm/<token>/', views.VerificationTokenApiView.as_view(), name='verification_token'),
    path('verification/resend/', views.ResendVerificationTokenApiView.as_view(), name='resend_verification_token'),
    # resend verification code
    # auth token login and logout
    # path('token/login/', views.CustomObtainAuthToken.as_view(), name='token_login'),
    # path('token/logout/', views.CustomDeleteAuthToken.as_view(), name='token_logout'),
    # jwt login
    path('jwt/create/', views.CustomTokenObtainPairView.as_view(), name='jwt_create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt_verify'),

    # profile
    path('profile/', views.ProfileApiView.as_view(), name='profile'),
]
