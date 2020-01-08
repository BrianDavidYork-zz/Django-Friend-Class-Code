from rest_framework import serializers
from Friend_Class.models import Friend


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
