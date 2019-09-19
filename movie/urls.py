from django.urls import path
from django.views.generic import RedirectView
from rest_framework.urlpatterns import format_suffix_patterns

from .views import MoviesListViewSet, TopMovieViewSet

urlpatterns = [
    path('movies/', MoviesListViewSet.as_view()),
    path('top/', TopMovieViewSet.as_view()),
    path('', RedirectView.as_view(url='/movies/')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
