from django.urls import path
from .views import PostView,SinglePostView,CommentView,SingleCommentView,\
    most_viewed_view, like_post_view

urlpatterns = [
    path('posts/', PostView.as_view()),
    path('posts/<slug:slug>/<str:publish_date>/', SinglePostView.as_view(), name='SinglePostView'),
    path('comments/', CommentView.as_view()),
    path('comments/<int:pk>', SingleCommentView().as_view()),
    path('posts/most_viewed', most_viewed_view),
    path('posts/like', like_post_view),
]