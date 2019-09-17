from django.test import TestCase

from ..models import Director, Movie
from ..serializers import DirectorSerializer, TopMoviesSerializer


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

