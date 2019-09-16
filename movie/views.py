from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Movie
from .serializers.movie_serializer import MovieSerializer


class MoviesList(APIView):

    def get(self, request, format=None):
        movies = Movie.objects.all().order_by('title')
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        movie_title = request.data['title']
        print(movie_title)
        movie = Movie.objects.filter(title=movie_title).first()
        if movie:
            return Response(request.data, status=status.HTTP_409_CONFLICT)
        return Response(request.data)
