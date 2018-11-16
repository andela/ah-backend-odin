from rest_framework import serializers

from .models import Follow

class UserFollowerSerializer(serializers.ModelSerializer):
    # serializer to format the instance to JSON
    class Meta:
        model = Follow

        fields = ('id','username','follows', 'follow_time')

        read_only_fields = ["follow_time"]

class UsersBeingFollowedSerializer(serializers.ModelSerializer):
    # serializer to format the instance to JSON
    class Meta:
        model = Follow

        fields = ('follows')

class UsersFollowingUserSerializer(serializers.ModelSerializer):
    # serializer to format the instance to JSON
    class Meta:
        model = Follow
        fields = ['follows']