from django.shortcuts import render
from django.core import serializers
from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from Friend_Class.models import User, Friend
from Friend_Class.serializers import FriendSerializer
from rest_framework.views import APIView


class FriendView(APIView):
    # Create Friendship
    def post(self, request, username):
        # static variables
        NO_FRIEND = 0
        USER_EQUALS_FRIEND = -1
        ALREADY_FRIENDS = -2
        REQUEST_PENDING = -3
        REPEAT_REQUEST = -4

        current_user = request.user

        result = Friend.add_friend(current_user, username)

        if result == NO_FRIEND:
            content = {'Invalid Request': 'Enter a valid username'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        elif result == USER_EQUALS_FRIEND:
            content = {'Invalid Request': 'You Cannot Send A Friend Request to Yourself'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        elif result == ALREADY_FRIENDS:
            content = {'Invalid Request': 'You Are Already Friends with %s' % friend}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        elif result == REQUEST_PENDING:
            content = {'Invalid Request': '%s Has Already Sent You a Friend Request. Confirm Friendship at '
                                          'confirm_friend/%s' % (friend, friend)}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        elif result == REPEAT_REQUEST:
            content = {'Invalid Request': 'Friend Request Already Pending with %s' % friend}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        elif isinstance(result, Friend):
            return Response('Friend Request Sent From %s to %s' % (current_user, friend))

    # Delete Friendship
    def delete(self, request, username):
        # static variables
        FRIENDSHIP_DELETED = 1
        NO_FRIENDSHIP = 0
        NO_FRIEND = -1

        current_user = request.user

        result = Friend.delete_friendship(current_user, username)

        if result == NO_FRIEND:
            content = {'Invalid Request': 'Enter a valid username'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        elif result == NO_FRIENDSHIP:
            content = {'Friendship Does Not Exist': 'Please Enter the Name of a Friend'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        elif result == FRIENDSHIP_DELETED:
            return Response('Friendship Deleted Between %s and %s' % (current_user, friend))

    # Show all Friendships involving a user
    def get(self, request, username):
        # static variables
        NO_USER = -1

        all_friends = Friend.get_all_friendships(username)

        if all_friends == NO_USER:
            content = {'Invalid Request': 'Enter a valid username'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        elif isinstance(all_friends, QuerySet):
            serializer = FriendSerializer(all_friends, many=True)
            return JsonResponse(serializer.data, safe=False)

    # Confirm Friendship
    def put(self, request, username):
        # static variables
        CONFIRMED = 1
        NO_PENDING_REQUEST = 0
        NO_USER = -1

        current_user = request.user

        result = Friend.confirm_friend(current_user, username)

        if result == CONFIRMED:
            return Response('Friendship Confirmed between %s and %s' % (current_user, friend))
        elif result == NO_USER:
            content = {'Invalid Request': 'Enter a valid username'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        elif result == NO_PENDING_REQUEST:
            content = {'Invalid Username': 'No Pending Friend Request from %s to Confirm' % friend}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
