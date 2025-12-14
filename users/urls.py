from django.urls import path
from .views import *

urlpatterns = [
    # Authentication endpoints
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('refresh/', RefreshTokenAPI.as_view(), name='refresh-token'),
    
    # User profile endpoints
    path('user-data/', UserDataAPI.as_view(), name='user-data'),
    path('user-data/update/', UpdateUserAPI.as_view(), name='update-user'),
    path('change-password/', ChangePasswordAPI.as_view(), name='change-password'),
    
    # Skills endpoints
    path('skills/', SkillListCreateAPI.as_view(), name='skill-list-create'),
    path('skills/<int:pk>/', SkillDetailAPI.as_view(), name='skill-detail'),
    
    # CV endpoints
    path('cv/', CVAPI.as_view(), name='cv-api'),
]
