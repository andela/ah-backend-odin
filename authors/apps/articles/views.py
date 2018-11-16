import uuid
import json

import jwt
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from rest_framework import generics, status
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated
)
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from django.http import HttpResponse
from .filters import FilterArticles
from django.contrib import auth

from .pagination import ArticleLimitOffSetPagination
from ..authentication.backends import JWTAuthentication
from ..authentication.models import User
from .models import Article, BookmarkingArticles

from .renderers import ArticleJSONRenderer
from .serializers import (ArticleDetailSerializer,
                          CreateArticleAPIViewSerializer,
                          UpdateArticleAPIVIEWSerializer,
                          LikeArticleAPIViewSerializer)


from authors.settings import WPM
from django.shortcuts import render
from .models import Article, Rating
from .serializers import CreateArticleAPIViewSerializer,RatingsSerializer, UpdateArticleAPIVIEWSerializer,ArticleDetailSerializer,ArticleDetailSerializer

from authors.settings import SECRET_KEY
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from rest_framework import generics, status




from .serializers import (
    ArticleDetailSerializer,
    CreateArticleAPIViewSerializer,
    UpdateArticleAPIVIEWSerializer
)


class ListCreateArticleAPIView(generics.ListCreateAPIView):

    renderer_classes = (ArticleJSONRenderer, )
    serializer_class = CreateArticleAPIViewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = ArticleLimitOffSetPagination

    def get_queryset(self):
        return FilterArticles.by_request(self.request)

    def create(self, request):
        """This method creates user articles"""

        article = request.data.get('article', {})
        article['author'] = request.user

        slug = slugify(article["title"]).replace("_", "-")
        slug = slug + "-" + str(uuid.uuid4()).split("-")[-1]
        article["slug"] = slug

        the_full_sentence = "{} {}".format(article['title'], article['body'])

        words = the_full_sentence.split()

        number_of_words = len(words)

        minutes = round(number_of_words/WPM,0)

        if int(minutes) < 1:

            message = "Less than a minute"

        else:

            message = str(minutes)+ " Minutes"

        
        article['read_time'] = message

        serializer = self.serializer_class(data=article)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        data = serializer.data
        data["message"] = "Your Article has been created successfully"

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateDestroyArticleAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = UpdateArticleAPIVIEWSerializer
    detailSerializer = ArticleDetailSerializer

    def update(self, request, slug):
        """This method updates a user article"""

        article = request.data.get('article', {})
        article["author"] = request.user.pk

        article_instance = get_object_or_404(Article, slug=slug)
        slug = slugify(article["title"]).replace("_", "-")
        slug = slug + "-" + str(uuid.uuid4()).split("-")[-1]
        article["slug"] = slug

        the_full_sentence = "{} {}".format(article['title'], article['body'])

        words = the_full_sentence.split()

        number_of_words = len(words)

        minutes = round(number_of_words/WPM,0)

        if int(minutes) < 1:

            message = "Less than a minute"

        else:

            message = str(minutes)+ " Minutes"

        
        article["read_time"] = message


        token = request.META.get('HTTP_AUTHORIZATION', ' ').split(' ')[1]
        payload = jwt.decode(token, settings.SECRET_KEY, 'utf-8')
        author_name = payload['username']
        user = User.objects.filter(username=author_name).first()

        serializer = self.serializer_class(data=article)
        serializer.is_valid(raise_exception=True)
        if article_instance.author != user:
            raise PermissionDenied

        serializer.update_article(article, article_instance)
        data = serializer.data
        data["message"] = "Article updated successfully."

        return Response(data, status=status.HTTP_201_CREATED)

    def destroy(self, request, slug):
        """This method allows a user to delete his article"""

        article_instance = get_object_or_404(Article, slug=slug)
        if article_instance.author != request.user:
            raise PermissionDenied
        self.perform_destroy(article_instance)
        return Response(
            {"message": "Article is deleted"},
            status=status.HTTP_200_OK
        )

    def retrieve(self, request, slug):
        """This method allows a user to retrieve one article"""

        article_instance = get_object_or_404(Article, slug=slug)
        serializer = self.detailSerializer()
        serializer.instance = article_instance
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookMarkArticleAPIView(generics.ListCreateAPIView):

    renderer_classes = (ArticleJSONRenderer, )
    queryset = Article.objects.all()
    permission_classes = (IsAuthenticated,)
    model = BookmarkingArticles

    def post(self, request, slug):

        user = request.user

        article_id = get_object_or_404(Article, slug=slug)

        # Trying to get a bookmark from the table, or create a new one
        bookmark, created = self.model.objects.get_or_create(
            user=user, article_id=article_id)
        # If no new bookmark has been created,
        # Then we believe that the request was to delete the bookmark
        if not created:
            bookmark.delete()

        return HttpResponse(
            json.dumps({
                "result": created,
                "count": self.model.objects.filter(article_id=article_id).count()
            }),
            content_type="application/json"
        )


class LikeArticleAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = LikeArticleAPIViewSerializer

    def post(self, request, slug):

        """This method allows user to like and dislike an article"""

        like = request.data.get('article', {})

        user_info = JWTAuthentication().authenticate(request)
        like["author"] = user_info[0].pk

        article_instance = get_object_or_404(Article, slug=slug)
        like["article"] = article_instance.pk
        
        serializer = self.serializer_class(data=like)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        if serializer.action_performed == "created":
            action_status = status.HTTP_201_CREATED
        else:
            action_status = status.HTTP_201_CREATED
        return Response(serializer.data, status=action_status)
class CreateRatings(generics.CreateAPIView):

    serializer_class = RatingsSerializer

    lookup_url_kwarg = 'slug'

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):

        slug = self.kwargs.get(self.lookup_url_kwarg)

        article_instance = Article.objects.get(slug=slug)

        article_id = article_instance.id

        article_author = article_instance.author_id

        article_rate = request.data.get('article_rate')

        if not article_rate:

            return Response({"Message": "You must provide a rating for this article"}, status=status.HTTP_400_BAD_REQUEST)
        if int(article_rate) >5 or int(article_rate) < 1:

            return Response({"Message": "You must provide a rating between 1 and 5"}, status=status.HTTP_400_BAD_REQUEST)

        user_instance = request.user

        username = user_instance.username

        user_instance = User.objects.get(username=username)

        user_id = user_instance.id


        rating_body = {

            "article": article_id,

            "article_rate": article_rate,

            "author": user_id
        }

        if article_author == user_id:

            return Response({"message": "You cannot rate your own article"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            serializer = self.serializer_class(data=rating_body)

            serializer.is_valid(raise_exception=True)

            serializer.save()

            data = serializer.data
            
            data["message"] = "You Have Successfully Rated This Article"

            return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveRatings(generics.RetrieveAPIView):

    lookup_url_kwarg = 'slug'
    
    serializer_class = RatingsSerializer

    def get_queryset(self, *args, **kwargs):

        slug = self.kwargs.get(self.lookup_url_kwarg)

        article_instance = Article.objects.get(slug=slug)

        article_id = article_instance.id

        article_ratings = Rating.objects.filter(article=article_id)
        
        return article_ratings

    def retrieve(self, *args, **kwargs):

        article_ratings = self.get_queryset()

        body = []

        article_title = {}

        article_rate = {}

        total_rates = 0

        ratings_count = article_ratings.count()

        for each_rate in article_ratings:

            title = Article.objects.get(id=each_rate.article_id)

            article_title['title'] = title.title

            total_rates = total_rates + each_rate.article_rate

        if ratings_count >0:

            average = round(total_rates/ratings_count,1)
            
            article_rate['rating'] = average

            combined_dict = {**article_title, **article_rate}

            body.append(combined_dict)

        return Response({"Article":body}, status=status.HTTP_200_OK)

class RetrieveAllArticlesWithRatings(generics.RetrieveAPIView):
    serializer_class = RatingsSerializer

    def get_queryset(self):

        article_instance = Article.objects.all()

        return article_instance

    def retrieve(self, *args, **kwargs):

        articles = self.get_queryset()

        body = []

        article_title = {}

        article_rate = {}

        for each_article in articles:

            article_id = each_article.id

            article_ratings = Rating.objects.filter(article=article_id)

            if article_ratings:

                total_rates = 0

                ratings_count = article_ratings.count()
                
                for each_rate in article_ratings:

                    article_instance = Article.objects.get(id=article_id)

                    article_title['title'] = article_instance.title

                    total_rates = total_rates + each_rate.article_rate

                if ratings_count >0:

                    average = round(total_rates/ratings_count,1)
                
                    article_rate['rating'] = average

                    combined_dict = {**article_title, **article_rate}

                    body.append(combined_dict)

            else:

                article_instance = Article.objects.get(id=article_id)

                article_title['title'] = article_instance.title  

                average = "Unknown"
                
                article_rate['rating'] = average

                combined_dict = {**article_title, **article_rate}

                print(combined_dict)

                body.append(combined_dict)
            
        return Response({"Article":body}, status=status.HTTP_200_OK)

