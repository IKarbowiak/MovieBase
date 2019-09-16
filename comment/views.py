from rest_framework import generics
from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework import status

from .models import Comment
from .serializers import CommentSerializer


class CommentFilter(filters.FilterSet):
    movie_id = filters.NumberFilter(field_name='movie__id')

    class Meta:
        model = Comment
        fields = ['movie_id']


class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = CommentFilter
    queryset = Comment.objects.all()

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = CommentSerializer(data=request.data, many=False)
        print(serializer.is_valid())
        if serializer.is_valid():
            print("Here")
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
