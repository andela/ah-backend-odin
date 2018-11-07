from rest_framework import serializers
from .models import Article
from ..authentication.models import User
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

class CreateArticleAPIViewSerializer(TaggitSerializer,serializers.ModelSerializer):
    tags = TagListSerializerField()
    author = serializers.SerializerMethodField()

    def get_author(self,obj):
        user = {
            "username":obj.author.username,
            "email":obj.author.email
        }
        return user


    class Meta:
        model = Article

        fields = ['title','description', 'body', 'author', 
                    'created_at', 'updated_at', 'tags', 'slug', 'published', 'image']

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

class UpdateArticleAPIVIEWSerializer(serializers.ModelSerializer):
    # user_id = User.pk

    class Meta:
        model = Article

        fields = ['title','description', 'body', 'author', 
                    'created_at', 'updated_at', 'tags', 'slug', 'published', 'image']

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

    def update_article(self,validated_data, article_instance):
        
        print(article_instance)
        article_instance.title = validated_data.get('title')
        article_instance.body = validated_data.get('body')
        article_instance.description = validated_data.get('description')
        article_instance.image = validated_data.get('image')
        article_instance.tags = validated_data.get('tags')
        article_instance.save()
        
        return article_instance
        