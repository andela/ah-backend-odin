from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('bio', 'image', 'username',)
        # we don't expect a user to update the username
        read_only_fields = ("username",)
