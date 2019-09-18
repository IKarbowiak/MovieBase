from django.test import TestCase

from movie.models import Movie
from ..models import Comment
from ..serializers import CommentSerializer


class CommentSerializerTest(TestCase):

    def test_contains_expected_fields_for_correct_data_with_instance(self):
        # GIVEN
        data = {'body': 'Test comment body'}
        movie = Movie.objects.create(title='TestTitle1', year=111, plot='TetPlot1', genre='TestGenre')
        comment = Comment.objects.create(movie=movie, **data)

        # WHEN
        serializer = CommentSerializer(instance=comment)

        # THEN
        data['movie_id'] = movie.id
        self.assertDictEqual(serializer.data, data)

    def test_contains_expected_fields_for_correct_data_with_data(self):
        # GIVEN
        data = {'body': 'Test comment body', 'movie_id': 1}

        # WHEN
        serializer = CommentSerializer(data=data)

        # THEN
        self.assertTrue(serializer.is_valid())
        self.assertDictEqual(serializer.data, data)

    def test_errors_fields_for_incorrect_data(self):
        # GIVEN
        data = {'body': 'Test comment body', 'movie_id': 'xyz'}

        # WHEN
        serializer = CommentSerializer(data=data)

        # THEN
        self.assertFalse(serializer.is_valid())
        self.assertSetEqual(set(serializer.errors), {'movie_id'})

    def test_save_for_correct_data(self):
        # GIVEN
        data = {'body': 'Test comment body', 'movie_id': 1}
        movie = Movie.objects.create(title='TestTitle1', year=111, plot='TetPlot1', genre='TestGenre')
        movie.pk = 1
        movie.save()

        # WHEN
        serializer = CommentSerializer(data=data)
        serializer.is_valid()
        serializer.save()

        # THEN
        comments = Comment.objects.all()
        self.assertEqual(comments.count(), 1)

        comment = comments[0]
        self.assertEqual(comment.body, data['body'])
        self.assertEqual(comment.movie.id, data['movie_id'])
