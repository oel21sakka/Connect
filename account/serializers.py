from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from rest_framework.validators import UniqueValidator

class ProfileSerializer(serializers.Serializer):
    avatar = serializers.ImageField(required = False)
    bio = serializers.CharField(required=False)

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all(),message='A user with that username already exists.')]
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(),message='A user with that email already exists.')]
    )
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    profile = ProfileSerializer()

    class Meta:
        fields = '__all__'
    
    def update(self, instance, validated_data):
        user_data=validated_data
        if 'profile' in user_data:
            profile_data = user_data.pop('profile')
            Profile.objects.filter(user=instance.id).update(**profile_data)
        User.objects.filter(id=instance.id).update(**user_data)
        return User.objects.get(id=instance.id)

class RegisterUserSerializer(UserSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    
    def create(self,validated_data):
        user_data=validated_data
        profile_data = user_data.pop('profile')
        user = User.objects.create_user(**user_data)
        Profile.objects.create(user=user,**profile_data)
        return User.objects.get(id=user.id)