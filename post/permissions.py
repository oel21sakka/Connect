from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission,SAFE_METHODS
from .models import Post

class PostPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            post = get_object_or_404(Post.objects.all(), slug=view.kwargs['slug'],
                                          publish_date=view.kwargs['publish_date'])
            return post.user.id==view.request.user.id or view.request.user.is_staff