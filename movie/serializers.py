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
    comment_count = serializers.SerializerMethodField()
    rank = serializers.IntegerField()

    class Meta:
        model = Movie
        fields = ['id', 'comment_count', 'rank']

    def get_comment_count(self, obj):
        return obj.comments.all().count()
