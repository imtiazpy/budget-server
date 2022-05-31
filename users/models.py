from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomBaseUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("User must have an email address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save()

        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Model for the User. We're creating a Custom User model with our own required fields
    """
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects: BaseManager[Any]

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name'] #email is required by default.

    def get_full_name(self):
        return self.name

    def __str__(self):
        return self.email
