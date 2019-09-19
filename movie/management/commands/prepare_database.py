import datetime

from django.core.management.base import BaseCommand

from ...models import Movie, Director
from comment.models import Comment


movie_data = [{
            "title": "Gladiator",
            "year": 2000,
            "genre": "Action, Adventure, Drama",
            "plot": "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered "
                    "his family and sent him into slavery.",
            "directors": [
                {
                    "full_name": "Ridley Scott"
                }
            ]
        },
        {
            "title": "The Godfather",
            "year": 1972,
            "genre": "Crime, Drama",
            "plot": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire "
                    "to his reluctant son.",
            "directors": [
                {
                    "full_name": "Francis Ford Coppola"
                }
            ]
        },
        {
            "title": "The Pianist",
            "year": 2002,
            "genre": "Biography, Drama, Music, War",
            "plot": "A Polish Jewish musician struggles to survive the destruction of the Warsaw ghetto of "
                    "World War II.",
            "directors": [
                {
                    "full_name": "Roman Polanski"
                }
            ]
        },
        {
            "title": "Titanic",
            "year": 1997,
            "genre": "Drama, Romance",
            "plot": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, "
                    "ill-fated R.M.S. Titanic.",
            "directors": [
                {
                    "full_name": "James Cameron"
                }
            ]
        }]


class Command(BaseCommand):

    def create_comment(self, movie, date_to_update=datetime.datetime.now(), body=''):
        if not body:
            body = 'Comment for movie {}'.format(movie.pk)
        comment = Comment.objects.create(movie=movie, body=body)
        comment.created_date = date_to_update
        comment.save()


    def handle(self, *args, **kwargs):
        existing_titles = Movie.objects.values_list('title', flat=True)
        for data in movie_data:
            directors = data.pop('directors')
            if data['title'] in existing_titles:
                continue
            movie = Movie.objects.create(**data)
            for director_data in directors:
                director, _ = Director.objects.get_or_create(**director_data)
                director.movies.add(movie)

        movies = Movie.objects.all()


        self.create_comment(movies[0], datetime.date(1990, 5, 15))
        self.create_comment(movies[1], datetime.date(1990, 5, 20))
        self.create_comment(movies[1], datetime.date(1990, 6, 27), 'Another comment for {}'.format(movies[1].pk))
        self.create_comment(movies[2], datetime.date(1990, 6, 11))
        self.create_comment(movies[2], datetime.date(1990, 4, 6), 'Another comment for'.format(movies[2].pk))

