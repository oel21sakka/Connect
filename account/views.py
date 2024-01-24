from rest_framework import generics, status
from .serializers import UserSerializer, RegisterUserSerializer
from django.contrib.auth.models import User
from .permissions import EditDestroyPersonalAccount
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.select_related('profile').all()
    serializer_class = RegisterUserSerializer
    
class UserView(generics.ListCreateAPIView):
    queryset = User.objects.select_related('profile').all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['@first_name', '@last_name']
    
class SingleUserView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [EditDestroyPersonalAccount]
    serializer_class = UserSerializer
    
    def get_queryset(self, *args, **kwargs):
        return User.objects.select_related('profile').filter(id=self.kwargs['pk'])

@api_view(['GET','DELETE'])
@permission_classes([IsAuthenticated])
def follow_user_view(request):
    if not 'user_id' in request.query_params:
        return Response({'error': 'user_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
    if request.method=='GET':
        request.user.profile.following.add(request.query_params['user_id'])
        return Response('user followed', status=status.HTTP_200_OK)
    else:
        request.user.profile.following.remove(request.query_params['user_id'])
        return Response('user unfollowed', status=status.HTTP_200_OK)

