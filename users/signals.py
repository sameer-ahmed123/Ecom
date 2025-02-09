from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from users.models import Profile


@receiver(post_save, sender=User)
def Create_user_profile(sender, instance, created, **kwargs):
    if created:
        prof = Profile.objects.create(user=instance)
        prof.auto_generate_generic_avatar()
        prof.save()


@receiver(post_delete, sender=User)
def Delete_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.delete()
    except Profile.DoesNotExist:
        pass
