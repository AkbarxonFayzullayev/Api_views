from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'movies', MovieViewSet)  # movies endpoint

urlpatterns = [
    path('router/', include(router.urls)),
    path('create_movie/',MovieCreateView.as_view()),
    path('movies/<int:pk>/add_actor/',MovieViewSet.as_view({'post': 'add_actor'})),
    path('actors/create/', ActorCreateView.as_view(), name='actor-create'),
    path('actors_api/', ActorApi.as_view()),

]
