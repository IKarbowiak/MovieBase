from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import MoviesListViewSet, TopMovieViewSet

urlpatterns = [
    path('movies/', MoviesListViewSet.as_view()),
    path('top/', TopMovieViewSet.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
