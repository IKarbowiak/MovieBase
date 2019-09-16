import requests

from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from .models import Movie
from .serializers import MovieSerializer
from moviebase.settings import OMDBAPI_KEY


# TODO !! Put somewhere else aPI key!!!

class MoviesList(generics.ListCreateAPIView):
    omdbapi_url = 'http://www.omdbapi.com/?apikey={}&t={}'
    queryset = Movie.objects.all().order_by('title')
    serializer_class = MovieSerializer


    def post(self, request, *args, **kwargs):
        movie_title = request.data['title']

        movie = Movie.objects.filter(title=movie_title).first()
        if movie:
            return Response(status=status.HTTP_409_CONFLICT)
        movie_detail = requests.get(self.omdbapi_url.format(OMDBAPI_KEY, movie_title)).json()

        if movie_detail['Response'] == 'False':
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(data=self.prepare_data_for_serializer(movie_detail))

        if serializer.is_valid():
            serializer.save()
            return Response({'movie_object': serializer.data, 'externalAPI_data': movie_detail})

        return Response(status=status.HTTP_417_EXPECTATION_FAILED)

    @staticmethod
    def prepare_data_for_serializer(external_api_data):
        required_fields = ['Title', 'Year', 'Genre', 'Director', 'Plot']
        data = {}
        for key, value in external_api_data.items():
            if key not in required_fields:
                continue
            if key == 'Director':
                key = 'directors'
                value = [{'full_name': name} for name in value.split(', ')]
            data[key.lower()] = value
        return data


