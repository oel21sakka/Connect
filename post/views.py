from http.client import responses
from rest_framework import generics
from .models import Post
from .serializers import PostSerializer, SinglePostSerializer
from .permissions import PostPermission

class PostView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SinglePostView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = SinglePostSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    permission_classes = [PostPermission]
