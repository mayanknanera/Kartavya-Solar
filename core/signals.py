from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Cart

User = get_user_model()


@receiver(post_save, sender=User)
def create_cart_for_new_user(sender, instance, created, **kwargs):
    """Automatically create a cart when a new user registers."""
    if created:
        Cart.objects.get_or_create(user=instance)
