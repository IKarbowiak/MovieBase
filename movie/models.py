from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    genre = models.CharField(max_length=100)
    plot = models.TextField()


class Director(models.Model):
    full_name = models.CharField(max_length=50)
    movies = models.ManyToManyField(Movie, related_name='directors')


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
