from django.urls import path
from .views import PostView,SinglePostView

urlpatterns = [
    path('', PostView.as_view()),
    path('<slug:slug>/<str:publish_date>/', SinglePostView.as_view(), name='SinglePostView')
]