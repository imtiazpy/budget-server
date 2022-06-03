from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from users.models import Profile

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    """Serializer for User creation and retrieve"""
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'name', 'email', 'password')


class ProfileSerializer(serializers.ModelSerializer):
    """Serialzer for retrieve update and delete profile"""
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('owner', )

class AvatarUploadSerializer(serializers.ModelSerializer):
    """Serializer for uploading users image"""
    class Meta:
        model = User
        fields = ('avatar', )