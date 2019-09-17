from rest_framework import serializers

from .models import Movie, Director


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['full_name', ]


class MovieSerializer(serializers.ModelSerializer):
    directors = DirectorSerializer(many=True)

    class Meta:
        model = Movie
        fields = ['title', 'year', 'genre', 'plot', 'directors']

    def create(self, validated_data):
        directors = validated_data.pop('directors')
        movie = Movie.objects.create(**validated_data)
        for director_data in directors:
            director, _ = Director.objects.get_or_create(**director_data)
            director.movies.add(movie)
        return movie


class TopMoviesSerializer(serializers.ModelSerializer):
    total_comments = serializers.IntegerField()
    rank = serializers.IntegerField()
    movie_id = serializers.IntegerField(source='pk')

    class Meta:
        model = Movie
        fields = ['movie_id', 'total_comments', 'rank']
