from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import MoviesList

urlpatterns = [
    path('movies/', MoviesList.as_view()),
    # path('comments/', name='comments'),
    # path('top/', name='top'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
