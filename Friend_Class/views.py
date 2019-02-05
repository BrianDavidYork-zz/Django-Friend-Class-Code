from django.shortcuts import render
from django.core import serializers
from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from Friend_Class.models import User, Friend
from Friend_Class.serializers import UserSerializer, UserProfileSerializer, FriendSerializer
from rest_framework.views import APIView
from Friend_Class.helper_functions import get_user_and_friend, invalid_username, check_for_friendship, already_friends


class UserProfile(APIView):
    def get(self, request, username):
        try:
            current_user, friend = get_user_and_friend(request=request, username=username)
            serializer = UserProfileSerializer(friend)
            return JsonResponse(serializer.data, safe=False)
        except User.DoesNotExist:
            return invalid_username()


class AddFriend(APIView):
    def get(self, request, username):
        try:
            current_user, friend = get_user_and_friend(request=request, username=username)
            friend_query = check_for_friendship(current_user=current_user, friend=friend)

            if friend == current_user:
                content = {'Invalid Request': 'You Cannot Send A Friend Request to Yourself'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return invalid_username()

        # checks if the friendship already exists
        if (friend_query[2] or friend_query[5]):
            return already_friends(friend=friend)
        # checks if friend has already sent current_user a friend request
        if not friend_query[1]:
            try:
                f = Friend(friend_A=current_user, friend_B=friend, friend_status=Friend.A_REQUESTS_B)
                f.save()
                return Response('Friend Request Sent From %s to %s' % (current_user, friend))
            except IntegrityError:
                content = {'Invalid Request':'Friend Request Already Pending with %s' % friend}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            content = {'Invalid Request': '%s Has Already Sent You a Friend Request. Confirm Friendship at '
                                          'confirm_friend/%s' % (friend, friend)}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class DeleteFriend(APIView):
    def get(self, request, username):
        try:
            current_user, friend = get_user_and_friend(request=request, username=username)
            friend_query = check_for_friendship(current_user=current_user, friend=friend)
        except User.DoesNotExist:
            return invalid_username()
        # checks for current_user and friend as friend_A and Friend_B respectively
        if friend_query[2]:
            f = friend_query[2]
            f.delete()
            return Response('Friendship Deleted Between %s and %s' % (current_user, friend))
        # checks for current_user and friend as friend_B and friend_A respectively
        elif friend_query[5]:
            f = friend_query[5]
            f.delete()
            return Response('Friendship Deleted Between %s and %s' % (current_user, friend))
        else:
            content = {'Friendship Does Not Exist' : 'Please Enter the Name of a Friend'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class ShowFriends(APIView):
    def get(self, request, username):
        current_user = User.objects.get(username=username)
        fa = Friend.objects.filter(friend_A=current_user)
        fa1 = fa.filter(friend_status=1)
        fb = Friend.objects.filter(friend_B=current_user)
        fb1 = fb.filter(friend_status=1)
        all_friends = fa1 | fb1
        serializer = FriendSerializer(all_friends, many=True)
        return JsonResponse(serializer.data, safe=False)


class ConfirmFriend(APIView):
    def get(self, request, username):
        try:
            current_user, friend = get_user_and_friend(request=request, username=username)
            friend_query = check_for_friendship(current_user=current_user, friend=friend)
        except User.DoesNotExist:
            return invalid_username()

        if not (friend_query[2] or friend_query[5]):
            # if current_user and friend are not confirmed friends, then friend request will be confirmed and the
            # friend_status changed to FRIENDS.  friend_query[1][0] grabs the first (and only) object in which friend
            # has sent a friend request to current_user, and friend_status is still A_REQUESTS_B.
            try:
                f = friend_query[1][0]
                f.friend_status = Friend.FRIENDS
                f.save()
                return Response('Friendship Confirmed between %s and %s' % (current_user, friend))
            except IndexError:
                content = {'Invalid Username': 'No Pending Friend Request from %s to Confirm' % friend}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            return already_friends(friend=friend)
