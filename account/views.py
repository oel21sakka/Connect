from rest_framework import generics
from .serializers import UserSerializer, RegisterUserSerializer
from django.contrib.auth.models import User
from .permissions import EditDestroyPersonalAccount
from rest_framework import filters

class UserView(generics.ListCreateAPIView):
    queryset = User.objects.select_related('profile').all()
    serializer_class = RegisterUserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['@first_name', '@last_name']
    
class SingleUserView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [EditDestroyPersonalAccount]
    serializer_class = UserSerializer
    
    def get_queryset(self, *args, **kwargs):
        return User.objects.select_related('profile').filter(id=self.kwargs['pk'])