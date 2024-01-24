from django.urls import path
from .views import UserView,SingleUserView,RegisterUserView,follow_user_view
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('', RegisterUserView.as_view()),
    path('<int:pk>', SingleUserView.as_view()),
    path('users/', UserView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('users/follow', follow_user_view),
]