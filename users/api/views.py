from rest_framework import generics
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from users.api.serializers import ProfileSerializer, AvatarUploadSerializer


User = get_user_model()


class ProfileAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id, is_active=True)


class AvatarUploadView(generics.UpdateAPIView):
    serializer_class = AvatarUploadSerializer
    queryset = User.objects.all()

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id, is_active=True)
