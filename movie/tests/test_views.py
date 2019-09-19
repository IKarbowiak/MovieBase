import datetime
from unittest import mock

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from movie.models import Movie
from movie.views import MoviesListViewSet, TopMovieViewSet
from comment.models import Comment


factory = APIRequestFactory()

example_data = {"Title": "TestTitle", "Year": "1997", "Rated": "PG-13", "Released": "19 Dec 1997",
                "Runtime": "194 min", "Genre": "Drama, Romance", "Director": "James Cameron",
                "Writer": "James Cameron", "Actors": "Leonardo DiCaprio, Kate Winslet, "
                                                     "Billy Zane, Kathy Bates",
                "Plot": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard "
                        "the luxurious, ill-fated R.M.S. Titanic.", "Language": "English, Swedish, Italian",
                "Country": "USA", "Awards": "Won 11 Oscars. Another 111 wins & 77 nominations.",
                "Poster": "https://m.media-amazon.com/images/M/MV5BMDdmZGU3NDQtY2E5My00ZTliLWIzOTU"
                          "tMTY4ZGI1YjdiNjk3XkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_SX300.jpg",
                "Ratings": [{"Source": "Internet Movie Database", "Value": "7.8/10"},
                            {"Source": "Rotten Tomatoes", "Value": "89%"}, {"Source": "Metacritic",
                                                                            "Value": "75/100"}],
                "Metascore": "75", "imdbRating": "7.8", "imdbVotes": "967,946", "imdbID": "tt0120338",
                "Type": "movie", "DVD": "10 Sep 2012", "BoxOffice": "N/A", "Production": "Paramount Pictures",
                "Website": "http://www.titanicmovie.com/", "Response": "True"}


def mocked_requests_get(self, *args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    return MockResponse(example_data, 200)


def mocked_requests_response_false(self, *args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            json_data['Response'] = 'False'
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    return MockResponse(example_data, 200)


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

    @mock.patch('movie.views.requests')
    def test_post_method(self, requests_mock):
        # GIVEN
        requests_mock.get = mocked_requests_get

        # WHEN
        view = MoviesListViewSet.as_view()
        request = factory.post('/', data={'title': 'TestTitle'}, format='json')
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(set(response.data.keys()), {'movie_object', 'externalAPI_data'})
        self.assertEqual(Movie.objects.all().count(), 1)

        movie = Movie.objects.all()[0]
        self.assertEqual(movie.title, 'TestTitle')

    @mock.patch('movie.views.requests')
    def test_post_method_for_existing_title(self, requests_mock):
        # GIVEN
        requests_mock.get = mocked_requests_get
        Movie.objects.create(title='TestTitle', year=111, plot='TetPlot', genre='TestGenre')

        # WHEN
        view = MoviesListViewSet.as_view()
        request = factory.post('/', data={'title': 'TestTitle'}, format='json')
        response = view(request)

        self.assertEqual(response.status_code, 409)

    @mock.patch('movie.views.requests')
    def test_post_method_for_response_false_from_external_api(self, requests_mock):
        # GIVEN
        requests_mock.get = mocked_requests_response_false

        # WHEN
        view = MoviesListViewSet.as_view()
        request = factory.post('/', data={'title': 'TestTitle'}, format='json')
        response = view(request)

        self.assertEqual(response.status_code, 404)

    @mock.patch('movie.views.MovieSerializer')
    @mock.patch('movie.views.requests')
    def test_post_method_for_existing_title(self, requests_mock, serializer_mock):
        # GIVEN
        requests_mock.get = mocked_requests_get
        serializer_mock().is_valid = lambda: False

        # WHEN
        view = MoviesListViewSet.as_view()
        request = factory.post('/', data={'title': 'TestTitle'}, format='json')
        response = view(request)

        self.assertEqual(response.status_code, 417)

    def test_filter_by_title(self):
        # GIVEN
        movie1 = Movie.objects.create(title='TestTitle1', year=111, plot='TetPlot1', genre='TestGenre')
        movie2 = Movie.objects.create(title='OtherTitle', year=111, plot='TetPlot1', genre='TestGenre')
        movie3 = Movie.objects.create(title='TestTitle2', year=111, plot='TetPlot1', genre='TestGenre')

        # WHEN
        view = MoviesListViewSet.as_view()
        request = factory.get('/', {'title__iexact': 'testtitle1'})
        response = view(request)

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertSetEqual({res['title'] for res in response.data['results']}, {movie1.title})

    def test_filter_by_year(self):
        # GIVEN
        movie1 = Movie.objects.create(title='TestTitle1', year=111, plot='TetPlot1', genre='TestGenre')
        movie2 = Movie.objects.create(title='OtherTitle', year=435, plot='TetPlot1', genre='TestGenre')
        movie3 = Movie.objects.create(title='TestTitle2', year=200, plot='TetPlot1', genre='TestGenre')

        # WHEN
        view = MoviesListViewSet.as_view()
        request = factory.get('/', {'year__gte': 150})
        response = view(request)

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
        self.assertSetEqual({res['title'] for res in response.data['results']}, {movie2.title, movie3.title})

    def test_filter_by_genre(self):
        # GIVEN
        movie1 = Movie.objects.create(title='TestTitle1', year=111, plot='TetPlot1', genre='TestGenre1')
        movie2 = Movie.objects.create(title='OtherTitle', year=111, plot='TetPlot1', genre='OtherGenre')
        movie3 = Movie.objects.create(title='TestTitle2', year=111, plot='TetPlot1', genre='TestGenre1 and other')

        # WHEN
        view = MoviesListViewSet.as_view()
        request = factory.get('/', {'genre__icontains': 'testgenre1'})
        response = view(request)

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
        self.assertSetEqual({res['title'] for res in response.data['results']}, {movie1.title, movie3.title})


class TopMoviesViewSetTest(TestCase):
    def test_post_without_parameters(self):
        # GIVEN
        movie = Movie.objects.create(title='TestTitle1', year=111, plot='TetPlot1', genre='TestGenre')
        Comment.objects.create(movie=movie, body='Test comment')

        # WHEN
        view = TopMovieViewSet.as_view()
        request = factory.get('/', )
        response = view(request)

        # THEN
        self.assertEqual(response.status_code, 400)

    def test_post_with_parameters(self):
        # GIVEN
        movie = Movie.objects.create(title='TestTitle1', year=111, plot='TetPlot1', genre='TestGenre', pk=1)

        comment1 = Comment.objects.create(movie=movie, body='Test comment')
        comment1.created_date = datetime.date(1000, 1, 14)
        comment1.save()

        movie2 = Movie.objects.create(title='TestTitle2', year=111, plot='TetPlot1', genre='TestGenre', pk=2)

        comment2 = Comment.objects.create(movie=movie2, body='Test comment')
        comment2.created_date = datetime.date(1000, 1, 15)
        comment2.save()

        comment3 = Comment.objects.create(movie=movie2, body='Test comment')
        comment3.created_date = datetime.date(1000, 1, 17)
        comment3.save()

        movie3 = Movie.objects.create(title='TestTitle3', year=111, plot='TetPlot1', genre='TestGenre', pk=3)

        comment4 = Comment.objects.create(movie=movie3, body='Test comment')
        comment4.created_date = datetime.date(1000, 1, 17)
        comment4.save()

        comment5 = Comment.objects.create(movie=movie3, body='Test comment')
        comment5.created_date = datetime.date(1000, 1, 1)
        comment5.save()

        movie4 = Movie.objects.create(title='TestTitle4', year=111, plot='TetPlot1', genre='TestGenre', pk=4)

        # WHEN
        view = TopMovieViewSet.as_view()
        request = factory.get('/', {'date_from': '1000-1-12', 'date_to': '1000-1-20'})
        response = view(request)

        # THEN
        result = [{'movie_id': 2, 'total_comments': 2, 'rank': 1}, {'movie_id': 3, 'total_comments': 1, 'rank': 2}, 
                  {'movie_id': 1, 'total_comments': 1, 'rank': 2}, {'movie_id': 4, 'total_comments': 0, 'rank': 3}]
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(result, response.data)

