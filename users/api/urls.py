from django.urls import path

from users.api.views import ProfileAPIView, AvatarUploadView

app_name = "users"

urlpatterns = [
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('avatar-upload/', AvatarUploadView.as_view(), name='avatar-upload'),
]