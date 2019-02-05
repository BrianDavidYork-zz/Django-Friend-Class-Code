from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    birthdate = models.DateField(null=True)
    hometown = models.CharField(max_length=50)
    # further customize the User model here

    def __str__(self):
        return self.username

#Automatically generates an authorization Token whenever a user instance is saved.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Friend(models.Model):
    #static variables for friend_status attribute
    FRIENDS = 1
    A_REQUESTS_B = 2

    friend_A = models.ForeignKey(User, related_name='friend_A')
    friend_B = models.ForeignKey(User, related_name='friend_B')
    friend_status = models.IntegerField()

    def __str__(self):
        return '%s and %s friendship' % (self.friend_A, self.friend_B)

    class Meta:
        unique_together = ('friend_A', 'friend_B')
