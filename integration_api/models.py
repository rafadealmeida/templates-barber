from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    stripe_subscription_id = models.CharField("Id do Stripe", max_length=60, blank=True, default="")

    def __str__(self):
        return f"Perfil de {self.user.username}"


# Sinal: sempre que um User for criado, garanta um Profile associado
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.profile.save()
