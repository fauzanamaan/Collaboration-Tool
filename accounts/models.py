from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
# Creating a table for User Profile


class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(
        upload_to='media/profile', blank=True, null=True)

    instagram_url = models.URLField(max_length=255, blank=True, null=True)
    facebook_url = models.URLField(max_length=255, blank=True, null=True)
    twitter_url = models.URLField(max_length=255, blank=True, null=True)
    linkedin_url = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return (str(self.user))


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
