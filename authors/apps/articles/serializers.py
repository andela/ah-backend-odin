from rest_framework import serializers
from ..authentication.models import User
from .models import (Article, 
                    ArticleLikes, 
                    Thread, 
                    Comment,
                    FavoriteArticle, 
                    Rating,
                    LikeComment)
from rest_framework.validators import UniqueTogetherValidator
from ..authentication.serializers import UserSerializer
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

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
                        'slug', 'published', 'image', 'likescount', 'dislikescount', 'read_time', 'comments']


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
        
        
        


class CreateCommentAPIViewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id','body','article','createdAt','updatedAt','author', )
        read_only_fields = ('article', )

    def validate(self, data):
        comment = data.get('body', None)
        if len(comment) < 2:
            raise serializers.ValidationError(
                "Comment should have atlest 2 characters"
            )
        else:
            return {
            'body': comment,
            }
        

    def create(self, validated_data):  
        author = self.context["author"]
        article = self.context["article"]
        body = validated_data.get('body')        
        return Comment.objects.create(body=body, author=author, article=article)



class CreateThreadAPIViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ('id','body','author','comment','createdAt','updatedAt')
        read_only_fields = ('author', 'comment', )

    def validate(self, data):
        comment_thread = data.get('body', None)
        if len(comment_thread) < 2:
            raise serializers.ValidationError(
                "Comment should have atlest 2 characters"
            )
        else:
            return {
            'body': comment_thread,
            }

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


class CreateCommentAPIViewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id','body','article','createdAt','updatedAt','author', 'commentlikescount', 'commentdislikescount')
        read_only_fields = ('article', )

    def validate(self, data):
        comment = data.get('body', None)
        if len(comment) < 2:
            raise serializers.ValidationError(
                "Comment should have atlest 2 characters"
            )
        else:
            return {
            'body': comment,
            }
        

    def create(self, validated_data):  
        author = self.context["author"]
        article = self.context["article"]
        body = validated_data.get('body')        
        return Comment.objects.create(body=body, author=author, article=article)



class CreateThreadAPIViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ('id','body','author','comment','createdAt','updatedAt')
        read_only_fields = ('author', 'comment', )

    def validate(self, data):
        comment_thread = data.get('body', None)
        if len(comment_thread) < 2:
            raise serializers.ValidationError(
                "Comment should have atlest 2 characters"
            )
        else:
            return {
            'body': comment_thread,
            }
        
    def create(self, validated_data):  
        author = self.context["author"]
        comment = self.context["comment"]
        body = validated_data.get('body')        
        return Thread.objects.create(body=body, author=author, comment=comment)


class CommentLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = LikeComment
        fields = ['author', 'comment', 'like_status']

    def create(self, validated_data):
        try:
            self.instance = LikeComment.objects.filter(author=validated_data["author"],
                                        comment=validated_data["comment"])[0:1].get()
        except LikeComment.DoesNotExist:
            return LikeComment.objects.create(**validated_data)

        self.perform_update(validated_data)
        return self.instance

    def perform_update(self, validated_data):

        if self.instance.like_status == validated_data["like_status"]:
            self.instance.delete()
        else:
            self.instance.like_status = validated_data["like_status"]
            self.instance.save()

