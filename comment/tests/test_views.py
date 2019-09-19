from django.test import TestCase
from rest_framework.test import APIRequestFactory

from ..models import Comment
from ..views import CommentListView
from movie.models import Movie


factory = APIRequestFactory()


class CommentListViewTest(TestCase):
    def test_get_comments_list(self):
        # GIVEN
        movie = Movie.objects.create(title='TestTitle1', year=111, plot='TetPlot1', genre='TestGenre')
        Comment.objects.create(movie=movie, body='Test comment body 1')
        Comment.objects.create(movie=movie, body='Test comment body 2')

        # WHEN
        view = CommentListView.as_view()
        request = factory.get("/")
        response = view(request)

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)

    def test_post_with_correct_data(self):
        # GIVEN
        movie_id = 1
        movie = Movie.objects.create(title='TestTitle1', year=111, plot='TetPlot1', genre='TestGenre')
        movie.pk = movie_id
        movie.save()

        data = {'movie_id': movie_id, 'body': 'Test comment'}

        # WHEN
        view = CommentListView.as_view()
        request = factory.post('/', data=data, format='json')
        response = view(request)

        # THEN
        comments = Comment.objects.all()
        self.assertEqual(comments.count(), 1)

        data['created_date'] = comments[0].created_date.strftime("%Y-%m-%d %H:%M:%S.%f%z")

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(data, response.data)

    def test_post_with_incorrect_data(self):
        # GIVEN
        movie_id = 5
        movie = Movie.objects.create(title='TestTitle1', year=111, plot='TetPlot1', genre='TestGenre')
        movie.pk = movie_id

        # WHEN
        view = CommentListView.as_view()
        request = factory.post('/', data={'movie_id': 1, 'body': 'Test comment'}, format='json')
        response = view(request)

        # THEN
        self.assertEqual(response.status_code, 404)

    def test_filter_by_movie_id(self):
        # GIVEN
        movie_id = 1
        movie = Movie.objects.create(title='TestTitle1', year=111, plot='TetPlot1', genre='TestGenre')
        movie.pk = movie_id
        movie.save()

        movie2 = Movie.objects.create(title='TestTitle2', year=111, plot='TetPlot1', genre='TestGenre')
        movie2.pk = 2
        movie2.save()

        Comment.objects.create(movie=movie, body='Test comment body 1')
        Comment.objects.create(movie=movie2, body='Test comment body 2')

        # WHEN
        view = CommentListView.as_view()
        request = factory.get("/", {'movie_id': movie_id})
        response = view(request)

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)

    def test_filter_by_not_existing_movie_id(self):
        # GIVEN
        movie_id = 1
        movie = Movie.objects.create(title='TestTitle1', year=111, plot='TetPlot1', genre='TestGenre')
        movie.id = movie_id
        movie.save()

        movie2 = Movie.objects.create(title='TestTitle2', year=111, plot='TetPlot1', genre='TestGenre')
        movie2.pk = 2
        movie2.save()

        Comment.objects.create(movie=movie, body='Test comment body 1')
        Comment.objects.create(movie=movie2, body='Test comment body 2')

        # WHEN
        view = CommentListView.as_view()
        request = factory.get("/", {'movie_id': 5})
        response = view(request)

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 0)
        self.assertListEqual(response.data['results'], [])

