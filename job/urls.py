from django.urls import path
from .views import *

urlpatterns=[
    path('recommendations/',   JobRecommendationAPI.as_view(),   name='job-recommendations'),
]