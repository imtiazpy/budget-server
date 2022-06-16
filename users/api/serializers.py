from rest_framework import serializers
from rest_framework.response import Response
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from django.db import transaction
from users.models import Profile

User = get_user_model()


class UserSerializer(UserCreateSerializer):
    """Serializer for User creation and retrieve"""
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'name', 'email', 'password')



class ProfileFields(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('gender', 'city', 'country',)

class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for retrieve update and delete profile"""

    profile = ProfileFields()
    class Meta:
        model = User
        fields = ('name', 'avatar', 'profile', )
        # read_only_fields = ('owner', )
    
    @transaction.atomic
    def update(self, instance, validated_data):
        ModelClass = self.Meta.model
        profile = validated_data.pop('profile', {})
        ModelClass.objects.filter(id=instance.id).update(**validated_data)

        if profile:
            Profile.objects.filter(owner=instance).update(**profile)

        new_instance = ModelClass.objects.get(id=instance.id)
        return new_instance

class AvatarUploadSerializer(serializers.ModelSerializer):
    """Serializer for uploading users image"""
    class Meta:
        model = User
        fields = ('avatar', )