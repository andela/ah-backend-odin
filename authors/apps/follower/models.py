from django.db import models

from django.conf import settings
from django.db.models.signals import post_save

from ..profiles.models import Profile

# Create your models here.

class Follow(models.Model):
    username = models.ForeignKey(Profile, on_delete=models.CASCADE) # follower 
    follows = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followed_people') # followee
    follow_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.follows)


# def profile_was_created(sender, instance, created, ** kwargs):
#     """ Listens for when a profile is created"""
#     created and Follow.objects.create(username=instance)


# post_save.connect(profile_was_created, sender=Profile)