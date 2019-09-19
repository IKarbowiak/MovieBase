from datetime import datetime

from django.db.models import Count, F, Q
from django.db.models.expressions import Window
from django.db.models.functions.window import DenseRank
from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
import requests

from .models import Movie
from .serializers import MovieSerializer, TopMoviesSerializer
from moviebase.settings import OMDBAPI_KEY


class MovieFilter(filters.FilterSet):
    class Meta:
        model = Movie
        fields = {'title': ['exact', 'iexact', 'contains', 'icontains'],
                  'genre': ['exact', 'iexact',  'contains', 'icontains'],
                  'year': ['exact', 'contains', 'gte', 'lte', 'gt', 'lt']}


class MoviesListViewSet(generics.ListCreateAPIView):
    omdbapi_url = 'http://www.omdbapi.com/?apikey={}&t={}'
    queryset = Movie.objects.all().order_by('title')
    serializer_class = MovieSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = MovieFilter


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


class TopMovieViewSet(generics.ListAPIView):
    queryset = Movie.objects.all().prefetch_related('comments')
    serializer_class = TopMoviesSerializer

    def list(self, request, *args, **kwargs):
        date_from = request.query_params.get('date_from', None)
        date_to = request.query_params.get('date_to', None)
        if not date_from or not date_to:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        date_from = datetime.strptime(date_from, '%Y-%m-%d')
        date_to = datetime.strptime(date_to, '%Y-%m-%d')

        queryset = self.get_queryset()

        queryset = queryset.annotate(total_comments=Count('comments', filter=(Q(comments__created_date__gte=date_from)
                                                                              & Q(comments__created_date__lt=date_to))))\
            .order_by('-total_comments')\
            .annotate(rank=Window(expression=DenseRank(), order_by=F('total_comments').desc()))

        serializer = TopMoviesSerializer(queryset, many=True)
        return Response(serializer.data)
