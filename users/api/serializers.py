from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    """Serializer for User creation and retrieve"""
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'name', 'email', 'password')


class AvatarUploadSerializer(serializers.ModelSerializer):
    """Serializer for uploading users image"""
    class Meta:
        model = User
        fields = ('avatar', )