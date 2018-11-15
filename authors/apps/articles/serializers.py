from rest_framework import serializers
from taggit_serializer.serializers import (TaggitSerializer,
                                           TagListSerializerField)

from .models import Article, Rating



from .models import Article, FavoriteArticle
from ..authentication.models import User
from .models import Article, ArticleLikes


from rest_framework.validators import UniqueTogetherValidator

class CreateArticleAPIViewSerializer(TaggitSerializer,serializers.ModelSerializer):
    tagList = TagListSerializerField()
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
                    'created_at', 'updated_at', 'tagList', 'slug', 'published', 'image', 'likescount', 'dislikescount', 'read_time']

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

class ArticleDetailSerializer(serializers.ModelSerializer):


    tagList = TagListSerializerField()
    class Meta:
        model = Article

        fields = ['title','description', 'body', 'author', 
                    'created_at', 'updated_at', 'tagList', 
                        'slug', 'published', 'image', 'likescount', 'dislikescount', 'read_time']


class UpdateArticleAPIVIEWSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article

        fields = ['title','description', 'body', 'author', 
                    'created_at', 'updated_at', 'tagList', 'slug', 'published', 'image', 'read_time']

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
        
        article_instance.title = validated_data.get('title')
        article_instance.body = validated_data.get('body')
        article_instance.description = validated_data.get('description')
        article_instance.image = validated_data.get('image')
        article_instance.tagList = validated_data.get('tagList')
        article_instance.save()
        
        return article_instance      

class RatingsSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = Rating

        fields = ['id', 'article', 'article_rate', 'author']

        validators = [UniqueTogetherValidator(

            queryset=Rating.objects.all(),

            fields=('article', 'author',),

            message = ("You cannot rate this article more than once")

        )]


class LikeArticleAPIViewSerializer(serializers.ModelSerializer):


    action_performed = "created"

    class Meta:
        model = ArticleLikes
        fields = ['author', 'article', 'article_like']

    def create(self, validated_data):

        try:
            self.instance = ArticleLikes.objects.filter(author=validated_data["author"].id)[
                            0:1].get()
        except ArticleLikes.DoesNotExist:
            return ArticleLikes.objects.create(**validated_data)

        self.perform_update(validated_data)
        return self.instance

    def perform_update(self, validated_data):
        if self.instance.article_like == validated_data["article_like"]:
            self.instance.delete()
            self.action_performed = "deleted"
        else:
            self.instance.article_like = validated_data["article_like"]
            self.instance.save()
            self.action_performed = "updated"

class FavoriteArticlesSerializer(serializers.ModelSerializer):

    class Meta:

        model = FavoriteArticle

        fields = ('article', 'favorite_status', 'author', 'favorited_at', 'last_updated_at')
        
