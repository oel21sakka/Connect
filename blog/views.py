from rest_framework import generics
from .models import Post, Comment
from .serializers import PostSerializer, SinglePostSerializer, CommentSerializer, SingleCommentSerializer
from .permissions import PostPermission, CommentPermission
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class PostView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SinglePostView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = SinglePostSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    permission_classes = [PostPermission]


class CommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SingleCommentView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = SingleCommentSerializer
    permission_classes = [CommentPermission]