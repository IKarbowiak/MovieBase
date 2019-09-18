from django.test import TestCase

from ..models import Director, Movie
from ..serializers import DirectorSerializer, TopMoviesSerializer, MovieSerializer


class DirectorSerializerTest(TestCase):

    def test_contains_expected_fields_for_correct_data_with_instance(self):
        # GIVEN
        data = {'full_name': 'TestDirector'}
        director = Director.objects.create(**data)

        # WHEN
        serializer = DirectorSerializer(instance=director)

        # THEN
        self.assertDictEqual(serializer.data, data)

    def test_contains_expected_fields_for_correct_data_with_data(self):
        # GIVEN
        data = {'full_name': 'TestDirector'}

        # WHEN
        serializer = DirectorSerializer(data=data)

        # THEN
        self.assertTrue(serializer.is_valid())
        self.assertDictEqual(serializer.data, data)

    def test_errors_fields_for_incorrect_data(self):
        # GIVEN
        data = {'name': 'TestDirector'}

        # WHEN
        serializer = DirectorSerializer(data=data)

        # THEN
        self.assertFalse(serializer.is_valid())
        self.assertSetEqual(set(serializer.errors), {'full_name'})


class TopMovieSerializerTest(TestCase):
    def test_contains_expected_fields_for_correct_data(self):
        # GIVEN
        data = {'total_comments': 1, 'rank': 1, 'movie_id': 1}
        movie = Movie.objects.create(title='TestTitle', year=111, plot='TetPlot', genre='TestGenre')
        movie.pk = 1

        # WHEN
        serializer = TopMoviesSerializer(data=data)

        # THEN
        self.assertTrue(serializer.is_valid())
        self.assertDictEqual(serializer.data, data)

    def test_errors_fields_for_incorrect_data(self):
        # GIVEN
        data = {'total_comments': 'abc', 'rank': 'xyz', 'movie_id': 1}
        movie = Movie.objects.create(title='TestTitle', year=111, plot='TetPlot', genre='TestGenre')
        movie.pk = 1

        # WHEN
        serializer = TopMoviesSerializer(data=data)

        # THEN
        self.assertFalse(serializer.is_valid())
        self.assertSetEqual(set(serializer.errors), {'total_comments', 'rank'})


class MovieSerializerTest(TestCase):
    def test_contains_expected_fields_for_correct_data_with_instance(self):
        # GIVEN
        data = {'title': 'TestTitle', 'year': 111, 'plot': 'TetPlot', 'genre': 'TestGenre'}

        movie = Movie.objects.create(**data)
        director = Director.objects.create(full_name='TestName')
        director.movies.add(movie)

        # WHEN
        serializer = MovieSerializer(instance=movie)

        # THEN
        data['directors'] = [{'full_name': director.full_name}]
        self.assertDictEqual(data, serializer.data)

    def test_contains_expected_fields_for_correct_data_with_data(self):
        # GIVEN
        data = {'title': 'TestTitle', 'year': 111, 'plot': 'TetPlot', 'genre': 'TestGenre',
                'directors': [{'full_name': 'TestDirector'}]}

        # WHEN
        serializer = MovieSerializer(data=data)

        # THEN
        self.assertTrue(serializer.is_valid())
        self.assertDictEqual(data, serializer.data)

    def test_contains_expected_fields_for_incorrect_data(self):
        # GIVEN
        data = {'title': 'TestTitle', 'year': 'abc', 'plot': 'TetPlot', 'genre': 'TestGenre',
                'directors': ['TestDirector']}

        # WHEN
        serializer = MovieSerializer(data=data)

        # THEN
        self.assertFalse(serializer.is_valid())
        self.assertSetEqual(set(serializer.errors), {'year', 'directors'})

    def test_save_for_correct_data(self):
        # GIVEN
        director_name = 'TestDirector'
        data = {'title': 'TestTitle', 'year': 111, 'plot': 'TetPlot', 'genre': 'TestGenre',
                'directors': [{'full_name': director_name}]}

        # WHEN
        serializer = MovieSerializer(data=data)
        serializer.is_valid()
        serializer.save()

        # THEN
        movies = Movie.objects.all()
        self.assertEqual(movies.count(), 1)

        movie = movies[0]
        self.assertEqual(movie.title, data['title'])
        self.assertEqual(movie.year, data['year'])
        self.assertEqual(movie.plot, data['plot'])
        self.assertEqual(movie.genre, data['genre'])
        self.assertSetEqual({director.full_name for director in movie.directors.all()}, {director_name})
