from rest_framework import viewsets, status
from posts.models import Group, Post, Comment

from .serializers import CommentSerializer, GroupSerializer, PostSerializer

from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet

from rest_framework.exceptions import PermissionDenied


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, serializer):
        if serializer.author != self.request.user:
            raise PermissionDenied(status.HTTP_403_FORBIDDEN)
        super(PostViewSet, self).perform_destroy(serializer)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied(status.HTTP_403_FORBIDDEN)
        serializer.save(author=self.request.user)
        super().perform_update(serializer)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.select_related('author')

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied(status.HTTP_403_FORBIDDEN)
        post_id = self.kwargs.get('post_id')
        serializer.save(author=self.request.user,
                        post=get_object_or_404(Post, pk=post_id))
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        if serializer.author != self.request.user:
            raise PermissionDenied(status.HTTP_403_FORBIDDEN)
        super(CommentViewSet, self).perform_destroy(serializer)
