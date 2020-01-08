from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    birthdate = models.DateField(null=True)
    hometown = models.CharField(max_length=50)

    def __str__(self):
        return self.username


class Friend(models.Model):
    # static variables for friend_status attribute
    FRIENDS = 1
    A_REQUESTS_B = 2

    friend_A = models.ForeignKey(User, related_name='friend_A', on_delete=models.SET_NULL, null=True)
    friend_B = models.ForeignKey(User, related_name='friend_B', on_delete=models.SET_NULL, null=True)
    friend_status = models.IntegerField()

    class Meta:
        unique_together = ('friend_A', 'friend_B')

    def __str__(self):
        return '%s and %s friendship' % (self.friend_A, self.friend_B)

    @classmethod
    def add_friend(cls, current_user, username):
        # static variables
        NO_FRIEND = 0
        USER_EQUALS_FRIEND = -1
        ALREADY_FRIENDS = -2
        REQUEST_PENDING = -3
        REPEAT_REQUEST = -4

        # find friend user
        try:
            friend = User.objects.get(username=username)
        except User.DoesNotExist:
            return NO_FRIEND

        # check if current_user is same as friend
        if current_user == friend:
            return USER_EQUALS_FRIEND

        # check if already friends
        friendship = Friend.check_for_friendship(current_user, friend, 1)
        if friendship is not None:
            return ALREADY_FRIENDS

        # check if request pending from friend
        pending_friendship = Friend.objects.filter(friend_A=friend) \
            .filter(friend_B=current_user) \
            .filter(friend_status=2)
        if pending_friendship:
            return REQUEST_PENDING

        # check if request already sent to friend
        pending_request = Friend.objects.filter(friend_A=current_user) \
            .filter(friend_B=friend) \
            .filter(friend_status=2)
        if pending_request:
            return REPEAT_REQUEST

        # If all checks are cleared, return Friend object
        new_friendship = cls(friend_A=current_user, friend_B=friend, friend_status=Friend.A_REQUESTS_B)
        new_friendship.save()
        return new_friendship

    @staticmethod
    def delete_friendship(current_user, username):
        # static variables
        FRIENDSHIP_DELETED = 1
        NO_FRIENDSHIP = 0
        NO_FRIEND = -1

        # find friend user
        try:
            friend = User.objects.get(username=username)
        except User.DoesNotExist:
            return NO_FRIEND

        # Find friendship with either status, and delete it
        friendship_1 = Friend.check_for_friendship(current_user, friend, 1)
        if friendship_1 is not None:
            friendship_1.delete()
            return FRIENDSHIP_DELETED
        friendship_2 = Friend.check_for_friendship(current_user, friend, 2)
        if friendship_2 is not None:
            friendship_2.delete()
            return FRIENDSHIP_DELETED

        return NO_FRIENDSHIP

    @staticmethod
    def confirm_friend(current_user, username):
        # static variables
        CONFIRMED = 1
        NO_PENDING_REQUEST = 0
        NO_USER = -1

        # find friend user
        try:
            friend = User.objects.get(username=username)
        except User.DoesNotExist:
            return NO_USER

        # find pending requests made to current_user
        pending_request = Friend.objects.filter(friend_A=friend) \
            .filter(friend_B=current_user) \
            .filter(friend_status=2)

        if pending_request:
            friendship = pending_request.get()
            friendship.friend_status = Friend.FRIENDS
            friendship.save()
            return CONFIRMED
        else:
            return NO_PENDING_REQUEST

    @staticmethod
    def get_all_friendships(username):
        # static variables
        NO_USER = -1

        try:
            current_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return NO_USER

        # filters for friendships where current user ss friend_A
        fa = Friend.objects.filter(friend_A=current_user).filter(friend_status=1)

        # filters for friendships where current user is friend_B
        fb = Friend.objects.filter(friend_B=current_user).filter(friend_status=1)

        # queryset union
        all_friends = fa | fb

        return all_friends

    @staticmethod
    def get_all_friends(user):
        # get all confirmed friendships involving user
        friend_queryset = Friend.get_all_friendships(user.username)

        user_list = []

        # iterates through friendships and appends non-user friend instances to user_list
        for friend in friend_queryset:
            if friend.friend_A == user:
                user_list.append(friend.friend_B)
            else:
                user_list.append(friend.friend_A)

        # returns list of user instances
        return user_list

    @staticmethod
    def check_for_friendship(current_user, friend, friend_status):
        # looks for friendship where current_user=friend_A, friend=friend_B
        friendship1 = Friend.objects.filter(friend_A=friend)\
            .filter(friend_B=current_user)\
            .filter(friend_status=friend_status)
        # looks for friendship where friend=friend_A, current_user=friend_b
        friendship2 = Friend.objects.filter(friend_A=current_user)\
            .filter(friend_B=friend)\
            .filter(friend_status=friend_status)
        if friendship1:
            return friendship1
        elif friendship2:
            return friendship2
        else:
            return None
