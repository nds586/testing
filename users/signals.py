from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Customer, ServiceProvider, User


@receiver(post_save, sender=User)
def create_user_profile(sender, instance: User, created: bool, **kwargs) -> None:
    if not created:
        return

    if instance.user_type == User.UserType.CUSTOMER:
        Customer.objects.get_or_create(user=instance)
    elif instance.user_type == User.UserType.PROVIDER:
        ServiceProvider.objects.get_or_create(user=instance)
