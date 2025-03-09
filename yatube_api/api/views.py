from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.decorators import action

from posts.models import Comment, Group, Post, Follow
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer, GroupSerializer,
    PostSerializer, FollowSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    """
    Набор представлений для просмотра и
    редактирования экземпляров Post.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Набор представлений для просмотра и
    редактирования экземпляров Comment.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(
            post_id=self.kwargs['post_id']
        )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post_id=self.kwargs['post_id']
        )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Набор представлений для просмотра экземпляров Group."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthorOrReadOnly]


class FollowViewSet(viewsets.ModelViewSet):
    """
    Набор представлений для просмотра и
    редактирования экземпляров Follow.
    """
    serializer_class = FollowSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        following_username = request.query_params.get('search', None)
        if following_username is not None:
            queryset = self.get_queryset().filter(
                following__username__icontains=following_username
            )
        else:
            queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
