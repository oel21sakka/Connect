from rest_framework import generics
from .serializers import UserSerializer, RegisterUserSerializer
from django.contrib.auth.models import User
from .permissions import EditDestroyPersonalAccount

class UserView(generics.ListCreateAPIView):
    queryset = User.objects.select_related('profile').all()
    serializer_class = RegisterUserSerializer
    
class SingleUserView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [EditDestroyPersonalAccount]
    
    serializer_class = UserSerializer
    
    def get_queryset(self, *args, **kwargs):
        return User.objects.select_related('profile').filter(id=self.kwargs['pk'])