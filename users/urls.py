from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns=[
    path('register/',   RegisterAPI.as_view(),   name='register'),
    path('otpverification/',   OtpVerificationAPI.as_view(),   name='otpverification'),
    path('login/',   LoginAPI.as_view(),   name='login'),
    path('logout/',   LogoutAPI.as_view(),   name='logout'),
    path('forgotpasswordotp/',   ForgotPasswordOtpAPI.as_view(),   name='forgotpasswordotp'),
    path('forgotpasswordreset/',   ForgotPasswordResetAPI.as_view(),   name='forgotpasswordreset'),
    path('custom-refresh/', RefreshAccessTokenAPI.as_view(), name='custom_refresh_token'),
    path('user-data/', UserDataAPI.as_view(), name='user-data'),
    path('user-data/update/', UpdateUserAPI.as_view() , name="update-user"),
    path('user-data/deactivate/', DeactivateUserAPI.as_view(), name="deactivate-user"),
    path('skills/', SkillListCreateAPI.as_view(), name='skill-list-create'),
    path('skills/<int:pk>/', SkillDetailAPI.as_view(), name='skill-detail'),
    path('cv/', CVAPI.as_view(), name='cv-api'),
]