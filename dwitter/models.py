from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self", related_name="followed_by", symmetrical=False, blank=True
    )

    def __str__(self) -> str:
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        print("instance", instance)
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.add(instance.profile)
        user_profile.save()


class Dweet(models.Model):
    # related_name="dweets" allows you to access 
    # the dweet objects from the user side of 
    # the relationship through .dweets
    user = models.ForeignKey(User, related_name="dweets", on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return (f"{self.user.username} "
                f"{self.created_at:%Y-%m-%d %H:%M} "
                f"{self.body[:30]}..."
        )