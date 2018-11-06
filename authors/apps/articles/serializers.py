from rest_framework import serializers
from .models import Article
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

class CreateArticleAPIViewSerializer(TaggitSerializer,serializers.ModelSerializer):
    tags = TagListSerializerField()
    author = serializers.SerializerMethodField()

    def get_author(self,obj):
        user = {
            "username":obj.author.username,
            "email":obj.author.email,
            "bio":obj.author.bio,
            "image":obj.author.bio
        }
        return user


    class Meta:
        model = Article

        fields = ['description', 'body', 'author', 'created_at', 'updated_at', 'tags', 'slug', 'published', 'image']

    def validate_title(self, value):
        if len(value) > 50:
            raise serializers.ValidationError(
                'The title should not be more than 50 characters'
            )
        return value
    def validate_description(self, value):
        if len(value) > 200:
            raise serializers.ValidationError(
                'The article should not be more than 200 characters'
            )
        return value



        