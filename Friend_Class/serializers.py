from rest_framework import serializers
from Friend_Class.models import User, Friend


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'birthdate', 'hometown')

class FriendSerializer(serializers.ModelSerializer):
    friend_A = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',)
    friend_B = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',)

    class Meta:
        model = Friend
        fields = ('__all__')
