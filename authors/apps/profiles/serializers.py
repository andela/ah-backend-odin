from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('bio', 'image', 'username',)
        # we don't expect a user to update the username
        read_only_fields = ("username",)


class ProfileAvatarSerializer(serializers.Serializer):
    image = serializers.ImageField()

    def update(self, instance, validated_data):
        """ Updates the users profile image"""
        # clean up the existing image if any
        instance.image.delete(False)
        instance.image = validated_data.get("image")
        instance.save()
        return {"image": instance.image}
