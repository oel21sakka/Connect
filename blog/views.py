from rest_framework import generics, status
from .models import Post, Comment
from .serializers import PostSerializer, SinglePostSerializer, CommentSerializer, SingleCommentSerializer, SearchSerializer
from .permissions import PostPermission, CommentPermission
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.cache import cache
from django.conf import settings
from django.shortcuts import get_object_or_404

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
            views = cache.get_or_set(self.get_object().get_views_cach_key(),0)
            cache.set(self.get_object().get_views_cach_key(),views+1)
            settings.REDIS_CLIENT.zincrby('post_ranking', 1, self.get_object().id)
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

@api_view(['GET'])
def most_viewed_view(request):
    post_ranking = settings.REDIS_CLIENT.zrange('post_ranking', 0, -1, desc=True)[:10]
    post_ranking_ids = [int(id) for id in post_ranking]
    most_viewed_posts = list(Post.objects.filter(id__in=post_ranking_ids))
    serializer = PostSerializer(most_viewed_posts, many=True)
    ordered_posts = sorted(serializer.data, key=lambda x: post_ranking_ids.index(x['id']))
    return Response(ordered_posts, status=status.HTTP_200_OK)

@api_view(['GET','DELETE'])
@permission_classes([IsAuthenticated])
def like_post_view(request):
    print(request.query_params)
    post = get_object_or_404(Post, id=request.query_params['post_id'])
    if request.method=='GET':
        post.users_like.add(request.user)
        return Response('post liked', status=status.HTTP_200_OK)
    else:
        post.users_like.remove(request.user)
        return Response('post unliked', status=status.HTTP_200_OK)