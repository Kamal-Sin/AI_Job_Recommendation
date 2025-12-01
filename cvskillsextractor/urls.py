from django.urls import path
from .views import *

urlpatterns=[
    path('extract-skills/',   ExtractSkillsAPI.as_view(),   name='extract-skills'),
]