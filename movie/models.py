from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    genre = models.CharField(max_length=100)
    plot = models.TextField()

    def __str__(self):
        return self.title


class Director(models.Model):
    full_name = models.CharField(max_length=50)
    movies = models.ManyToManyField(Movie, related_name='directors')

    def __str__(self):
        return self.full_name
