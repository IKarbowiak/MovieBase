from unittest import mock

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from movie.models import Movie
from movie.views import MoviesListViewSet

factory = APIRequestFactory()


class MovieListViewSetTest(TestCase):
    def test_get_method(self):
        # GIVEN
        m1 = Movie.objects.create(title='TestTitle1', year=111, plot='TetPlot1', genre='TestGenre')
        m2 = Movie.objects.create(title='TestTitle2', year=111, plot='TetPlot2', genre='TestGenre')

        # WHEN
        view = MoviesListViewSet.as_view()
        request = factory.get("/")
        response = view(request)

        # THEN
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
        self.assertSetEqual({m1.title, m2.title}, {movie['title'] for movie in response.data['results']})
