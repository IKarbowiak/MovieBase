from rest_framework import serializers
from django.shortcuts import get_object_or_404

from .models import Comment
from movie.models import Movie


class CommentSerializer(serializers.ModelSerializer):
    movie_id = serializers.IntegerField()
    created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f%z", read_only=True)

    class Meta:
        model = Comment
        fields = ['movie_id', 'body', 'created_date']

    def create(self, validated_data):
        movie_id = validated_data.pop('movie_id')
        movie_obj = get_object_or_404(Movie, pk=movie_id)
        comment = Comment.objects.create(movie=movie_obj, **validated_data)
        return comment
