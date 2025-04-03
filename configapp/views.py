from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
# from rest_framework.generics import CreateAPIView
from .serializers import *


@api_view(["GET", "POST"])
def movie_api(request):
    if request.method == "GET":
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    if request.method == "POST":
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET","PUT", "PATCH", "DELETE"])
def movie_detail(request, slug):
    try:
        movie = Movie.objects.get(slug=slug)
    except Movie.DoesNotExist:
        return Response({"success": False, "error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)

    response = {"success": True}
    if request.method == "GET":
        actors = Movie.objects.all()
        serializer = MovieSerializer(actors, many=True)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response["data"] = serializer.data
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PATCH":
        serializer = MovieSerializer(movie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response["data"] = serializer.data
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        movie.delete()
        return Response({"success": True, "message": "Movie deleted"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def ism_api(request):
    name = request.data["name"]
    surname = request.data["surname"]
    birth_date = request.data["birth_date"]
    return Response(data={f"{name} {surname} , {birth_date}- yilda tug'ilgan"})


class ActorApi(APIView):
    def get(self,request):
        actors = Actor.objects.all()
        serializer = ActorSerializer(actors,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        data = {'success': True}
        serializer = ActorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data['data'] = serializer.data
            return Response(data=data,status=status.HTTP_200_OK)
        data['success'] = False
        return Response(data=data)

class ActorDetailApi(APIView):
    def get(self,request,pk):
        response = {'success':True}
        try:
            actor = Actor.objects.get(pk=pk)
            serializer = ActorSerializer(actor)
            response['data'] = serializer.data
            return Response(data=response)
        except Actor.DoesNotExist:
            response['success'] = False
            return Response(data=response)

class ActorCreateView(CreateAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    @action(detail=True,methods=['post'])
    def add_actor(self,request,pk):
        movie = self.get_object()
        actor_id = request.data.get('actor_id')

        if not actor_id:
            return Response({"error": "actor_id required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            actor = Actor.objects.get(id=actor_id)
        except Actor.DoesNotExist:
            return Response({"error": "Actor not found"}, status=status.HTTP_404_NOT_FOUND)
        movie.actors.add(actor)
        return Response({"message": f"Actor {actor.name} added to movie {movie.name}"}, status=status.HTTP_200_OK)


