from django.urls import path

from users.api.views import ProfileAPIView, AvatarUploadView, UserActivationView

app_name = "users"

urlpatterns = [
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('avatar-upload/', AvatarUploadView.as_view(), name='avatar-upload'),
    path('activate/<str:uid>/<str:token>', UserActivationView.as_view())
]