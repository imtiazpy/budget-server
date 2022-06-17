from django.urls import path

from users.api.views import ProfileAPIView, AvatarUploadView, UserActivationView, PasswordResetConfirmView

app_name = "users"

urlpatterns = [
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('avatar-upload/', AvatarUploadView.as_view(), name='avatar-upload'),
    path('activate/<str:uid>/<str:token>', UserActivationView.as_view()),
    path('password/reset/confirm/<str:uid>/<str:token>', PasswordResetConfirmView.as_view()),
]