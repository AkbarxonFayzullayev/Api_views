from rest_framework import serializers
from .models import *

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    actors = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Actor.objects.all()
    )
    class Meta:
        model = Movie
        fields = '__all__'
