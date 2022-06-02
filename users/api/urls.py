from django.urls import path

from users.api.views import AvatarUploadView

app_name = "users"

urlpatterns = [
    path('avatar-upload/', AvatarUploadView.as_view(), name='avatar-upload'),
]