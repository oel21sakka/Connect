from django.urls import path
from .views import UserView,SingleUserView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('', UserView.as_view()),
    path('<int:pk>', SingleUserView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
]