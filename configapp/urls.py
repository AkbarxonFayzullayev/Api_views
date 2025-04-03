from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'movies', MovieViewSet)  # movies endpoint

urlpatterns = [
    path('', include(router.urls)),
    path('actors/create/', ActorCreateView.as_view(), name='actor-create'),
    path('actors_api/', ActorApi.as_view()),
]
