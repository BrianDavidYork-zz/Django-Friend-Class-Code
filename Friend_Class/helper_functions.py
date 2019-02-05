from rest_framework.response import Response
from rest_framework import status
from Friend_Class.models import User, Friend


def get_user_and_friend(request, username):
    current_user = request.user
    friend = User.objects.get(username=username)
    return (current_user, friend)


def check_for_friendship(current_user, friend):
    f1 = Friend.objects.filter(friend_A=friend)
    f2 = f1.filter(friend_B=current_user)
    f3 = f2.filter(friend_status=Friend.FRIENDS)
    fa = Friend.objects.filter(friend_A=current_user)
    fb = fa.filter(friend_B=friend)
    fc = fb.filter(friend_status=Friend.FRIENDS)
    return (f1, f2, f3, fa, fb, fc)


def invalid_username():
    content = {'Invalid Username': 'Please Enter a valid Username'}
    return Response(content, status=status.HTTP_400_BAD_REQUEST)

def already_friends(friend):
    content = {'Invalid Request': 'You are already Friends with %s' % friend}
    return Response(content, status=status.HTTP_400_BAD_REQUEST)