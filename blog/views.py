from rest_framework import generics, status
from .models import Post, Comment
from .serializers import PostSerializer, SinglePostSerializer, CommentSerializer, SingleCommentSerializer, SearchSerializer
from .permissions import PostPermission, CommentPermission
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.cache import cache

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
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            post_id = self.get_object().id
            cache.incr(self.get_object().get_views_cach_key())
        return response


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

@api_view(['GET'])
def search_view(request):
    serializer=SearchSerializer(data=request.query_params)
    if serializer.is_valid():
        return Response(serializer.search(), status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)