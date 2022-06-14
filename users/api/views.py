from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
import requests

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
    

class UserActivationView(generics.GenericAPIView):
    """View to activate account upon clicking on the link from activation email"""
    permission_classes = [AllowAny]
    def get(self, request, uid, token, format=None):
        payload = {'uid': uid, 'token': token}
        url = 'http://127.0.0.1:8000/api/v1/auth/users/activation/'

        response = requests.post(url, data=payload)

        return redirect("http://localhost:3000/sign-in")

        # if response.status_code == 204:
        #     return Response({}, response.status_code)
        # else:
        #     return Response(response.json())
