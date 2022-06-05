from django.db.models.signals import post_save
from django.dispatch import receiver 
from django.contrib.auth import get_user_model

from users.models import Profile
from budget.models import Budget


User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create Profile and Budget upon user creation"""
    if created:
        Profile.objects.create(owner=instance)
        Budget.init_budget(instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()